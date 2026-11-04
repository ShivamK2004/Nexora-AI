from uuid import uuid4
import re
from backend.app.db import connect

def create_memory(content: str, category: str = "general") -> dict:
    memory_id = str(uuid4())
    with connect() as conn:
        conn.execute("INSERT INTO memories(id,content,category) VALUES(?,?,?)", (memory_id, content.strip(), category.strip() or "general"))
    return {"id": memory_id, "content": content.strip(), "category": category}

def list_memories() -> list[dict]:
    with connect() as conn:
        rows = conn.execute("SELECT id,content,category,created_at FROM memories ORDER BY created_at DESC").fetchall()
    return [dict(row) for row in rows]

def delete_memory(memory_id: str) -> bool:
    with connect() as conn:
        cur = conn.execute("DELETE FROM memories WHERE id=?", (memory_id,))
        return cur.rowcount > 0

def retrieve_memories(query: str, limit: int = 3) -> list[dict]:
    terms = {t.lower() for t in re.findall(r"[\w'-]+", query) if len(t) > 2}
    if not terms:
        return []
    items = list_memories()
    ranked = []
    for item in items:
        words = {t.lower() for t in re.findall(r"[\w'-]+", item["content"]) if len(t) > 2}
        score = len(terms & words) / len(terms)
        if score:
            ranked.append((score, item))
    ranked.sort(key=lambda x: x[0], reverse=True)
    return [item for _, item in ranked[:limit]]
