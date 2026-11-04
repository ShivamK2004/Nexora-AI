import hashlib
import json
import re
from pathlib import Path
from uuid import uuid4

from backend.app.config import get_settings
from backend.app.db import connect

WORD_RE = re.compile(r"[a-zA-Z0-9_'-]+")


def extract_text(filename: str, raw: bytes) -> str:
    suffix = Path(filename).suffix.lower()
    if suffix in {".txt", ".md", ".markdown", ".csv", ".json", ".py", ".sql"}:
        return raw.decode("utf-8", errors="replace")
    if suffix == ".pdf":
        try:
            from pypdf import PdfReader
            import io
            reader = PdfReader(io.BytesIO(raw))
            return "\n\n".join(page.extract_text() or "" for page in reader.pages)
        except Exception as exc:
            raise ValueError(f"Could not parse PDF: {exc}") from exc
    raise ValueError("Unsupported file type. Upload TXT, Markdown, CSV, JSON, Python, SQL, or PDF.")


def chunk_text(text: str, chunk_size: int = 900, overlap: int = 120) -> list[str]:
    text = re.sub(r"\s+", " ", text).strip()
    if not text:
        return []
    chunks, start = [], 0
    while start < len(text):
        end = min(len(text), start + chunk_size)
        if end < len(text):
            boundary = text.rfind(" ", start + int(chunk_size * 0.65), end)
            if boundary > start:
                end = boundary
        piece = text[start:end].strip()
        if piece:
            chunks.append(piece)
        if end >= len(text):
            break
        start = max(start + 1, end - overlap)
    return chunks


def _embed(texts: list[str]) -> list[list[float]] | None:
    model_name = get_settings().embedding_model
    if not model_name:
        return None
    try:
        from sentence_transformers import SentenceTransformer
        global _EMBEDDER
        try:
            encoder = _EMBEDDER
        except NameError:
            _EMBEDDER = SentenceTransformer(model_name)
            encoder = _EMBEDDER
        return encoder.encode(texts, normalize_embeddings=True).tolist()
    except ImportError as exc:
        raise RuntimeError(
            "Embedding model configured but sentence-transformers is not installed. "
            "See requirements-embeddings.txt"
        ) from exc


def ingest_document(filename: str, raw: bytes) -> dict:
    settings = get_settings()
    if len(raw) > settings.max_upload_mb * 1024 * 1024:
        raise ValueError(f"File exceeds {settings.max_upload_mb} MB limit")
    text = extract_text(filename, raw)
    parts = chunk_text(text)
    if not parts:
        raise ValueError("No extractable text found in the uploaded file")
    doc_id = str(uuid4())
    digest = hashlib.sha256(raw).hexdigest()
    vectors = _embed(parts)
    with connect() as conn:
        conn.execute(
            "INSERT INTO documents(id, filename, content_hash) VALUES(?,?,?)",
            (doc_id, Path(filename).name, digest),
        )
        for index, part in enumerate(parts):
            vector = json.dumps(vectors[index]) if vectors else None
            conn.execute(
                "INSERT INTO chunks(document_id, chunk_index, content, embedding_json) VALUES(?,?,?,?)",
                (doc_id, index, part, vector),
            )
    return {
        "id": doc_id, "filename": Path(filename).name, "chunks": len(parts),
        "characters": len(text), "embedding": bool(vectors),
    }


def list_documents() -> list[dict]:
    with connect() as conn:
        rows = conn.execute(
            "SELECT d.id,d.filename,d.created_at,COUNT(c.id) AS chunks "
            "FROM documents d LEFT JOIN chunks c ON c.document_id=d.id "
            "GROUP BY d.id ORDER BY d.created_at DESC"
        ).fetchall()
    return [dict(row) for row in rows]


def delete_document(doc_id: str) -> bool:
    with connect() as conn:
        cur = conn.execute("DELETE FROM documents WHERE id=?", (doc_id,))
        return cur.rowcount > 0


def retrieve(query: str, limit: int = 4) -> list[dict]:
    terms = {t.lower() for t in WORD_RE.findall(query) if len(t) > 2}
    if not terms:
        return []
    with connect() as conn:
        rows = conn.execute(
            "SELECT c.id,c.content,c.embedding_json,d.id AS document_id,d.filename "
            "FROM chunks c JOIN documents d ON d.id=c.document_id"
        ).fetchall()
    query_vector = None
    if rows and any(row["embedding_json"] for row in rows) and get_settings().embedding_model:
        try:
            query_vector = _embed([query])[0]
        except Exception:
            query_vector = None
    scored = []
    for row in rows:
        body_terms = {t.lower() for t in WORD_RE.findall(row["content"]) if len(t) > 2}
        lexical = len(terms & body_terms) / max(1, len(terms))
        semantic = 0.0
        if query_vector and row["embedding_json"]:
            vector = json.loads(row["embedding_json"])
            semantic = sum(a * b for a, b in zip(query_vector, vector))
        score = (0.55 * lexical + 0.45 * max(0.0, semantic)) if query_vector else lexical
        if score > 0:
            scored.append((score, row))
    scored.sort(key=lambda item: item[0], reverse=True)
    return [
        {
            "chunk_id": row["id"], "document_id": row["document_id"],
            "filename": row["filename"], "content": row["content"], "score": round(score, 4),
        }
        for score, row in scored[:limit]
    ]
