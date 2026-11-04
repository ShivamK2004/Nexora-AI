from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=12000)
    conversation_id: str | None = None


class ChatResponse(BaseModel):
    conversation_id: str
    answer: str
    provider: str
    citations: list[dict] = []


class MemoryCreate(BaseModel):
    content: str = Field(min_length=1, max_length=3000)
    category: str = Field(default="general", max_length=80)


class AgentRequest(BaseModel):
    task: str = Field(min_length=1, max_length=12000)
    agent: str | None = None
