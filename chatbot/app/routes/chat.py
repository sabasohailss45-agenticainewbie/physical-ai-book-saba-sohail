import asyncio
import logging
import uuid

from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import JSONResponse

from app.models import ChatRequest, ChatResponse, ErrorResponse, SourceChunk
from app.services.embedder import embed_text
from app.services.retriever import retrieve_chunks
from app.services.generator import generate_answer
from app.services.db import save_turn
from app.config import settings
from app.limiter import limiter

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/health")
async def health_check():
    return {"status": "ok"}


@router.post("/chat", response_model=ChatResponse)
@limiter.limit(f"{settings.rate_limit_per_minute}/minute")
async def chat(request: Request, body: ChatRequest):
    request_id = getattr(request.state, "request_id", str(uuid.uuid4()))

    try:
        # 1. Embed the question
        try:
            embedding = await embed_text(body.question)
        except Exception:
            return JSONResponse(
                status_code=503,
                content=ErrorResponse(
                    error="Service temporarily unavailable. Please try again later.",
                    request_id=request_id,
                ).model_dump(),
            )

        # 2. Retrieve relevant chunks
        chunks = await retrieve_chunks(embedding, top_k=5)

        # 3. Generate answer
        try:
            answer, usage = await generate_answer(body.question, chunks)
        except Exception:
            return JSONResponse(
                status_code=503,
                content=ErrorResponse(
                    error="Service temporarily unavailable. Please try again later.",
                    request_id=request_id,
                ).model_dump(),
            )

        # 4. Persist turn asynchronously (non-blocking, swallow errors)
        chunk_ids = [c["chunk_id"] for c in chunks]
        asyncio.create_task(
            save_turn(
                session_id=str(body.session_id),
                question=body.question,
                answer=answer,
                context_chunks=chunk_ids,
                usage=usage,
                model=settings.openai_chat_model,
            )
        )

        # 5. Build response
        sources = [
            SourceChunk(
                chunk_id=c["chunk_id"],
                chapter_slug=c["chapter_slug"],
                preview=c["content"][:100],
            )
            for c in chunks
        ]

        return ChatResponse(
            answer=answer,
            session_id=body.session_id,
            request_id=request_id,
            sources=sources,
        )

    except Exception as exc:
        logger.error("Unhandled error in /chat: %s", exc, exc_info=True)
        return JSONResponse(
            status_code=500,
            content=ErrorResponse(
                error="An unexpected error occurred.",
                request_id=request_id,
            ).model_dump(),
        )
