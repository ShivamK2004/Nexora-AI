from fastapi import APIRouter, HTTPException
from backend.app.schemas import AgentRequest
from backend.app.services.agents import run_agent, AGENTS
from backend.app.services.llm import LLMError
router = APIRouter(prefix="/api/agents", tags=["agents"])

@router.get("")
def list_agents():
    return [{"id":key,"description":value} for key,value in AGENTS.items()]

@router.post("/run")
async def execute_agent(payload: AgentRequest):
    try:
        return await run_agent(payload.task, payload.agent)
    except LLMError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
