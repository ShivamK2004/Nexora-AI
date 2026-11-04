from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from backend.app.services.tools import safe_calculate, current_time
router = APIRouter(prefix="/api/tools", tags=["tools"])
class CalcRequest(BaseModel):
    expression: str = Field(min_length=1, max_length=160)
@router.post("/calculate")
def calculate(payload: CalcRequest):
    try:
        return {"expression":payload.expression,"result":safe_calculate(payload.expression)}
    except (ValueError, ZeroDivisionError, OverflowError) as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
@router.get("/time")
def time_tool():
    return {"utc":current_time()}
