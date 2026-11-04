from fastapi import APIRouter, HTTPException
from backend.app.schemas import MemoryCreate
from backend.app.services.memory import create_memory, list_memories, delete_memory
router = APIRouter(prefix="/api/memories", tags=["memory"])

@router.post("")
def add_memory(payload: MemoryCreate):
    return create_memory(payload.content, payload.category)

@router.get("")
def get_memories():
    return list_memories()

@router.delete("/{memory_id}")
def remove_memory(memory_id: str):
    if not delete_memory(memory_id):
        raise HTTPException(status_code=404, detail="Memory not found")
    return {"deleted":True,"id":memory_id}
