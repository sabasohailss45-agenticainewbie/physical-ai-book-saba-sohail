from uuid import UUID
from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=2000)
    session_id: UUID


class SourceChunk(BaseModel):
    chunk_id: str
    chapter_slug: str
    preview: str


class ChatResponse(BaseModel):
    answer: str
    session_id: UUID
    request_id: str
    sources: list[SourceChunk] = []


class ErrorResponse(BaseModel):
    error: str
    request_id: str
