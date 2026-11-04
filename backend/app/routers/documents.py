from fastapi import APIRouter, UploadFile, File, HTTPException
from backend.app.services.knowledge import ingest_document, list_documents, delete_document
router = APIRouter(prefix="/api/documents", tags=["knowledge"])

@router.post("")
async def upload_document(file: UploadFile = File(...)):
    raw = await file.read()
    try:
        return ingest_document(file.filename or "upload.txt", raw)
    except (ValueError, RuntimeError) as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

@router.get("")
def get_documents():
    return list_documents()

@router.delete("/{document_id}")
def remove_document(document_id: str):
    if not delete_document(document_id):
        raise HTTPException(status_code=404, detail="Document not found")
    return {"deleted":True,"id":document_id}
