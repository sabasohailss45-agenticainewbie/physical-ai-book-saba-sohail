import json
import logging
import asyncpg
from app.config import settings

logger = logging.getLogger(__name__)
_pool: asyncpg.Pool | None = None

DDL = """
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

CREATE TABLE IF NOT EXISTS conversation_turns (
    id                UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id        UUID        NOT NULL,
    question          TEXT        NOT NULL CHECK (char_length(question) <= 2000),
    answer            TEXT        NOT NULL,
    context_chunks    JSONB       NOT NULL DEFAULT '[]',
    prompt_tokens     INTEGER     NOT NULL DEFAULT 0,
    completion_tokens INTEGER     NOT NULL DEFAULT 0,
    total_tokens      INTEGER     NOT NULL DEFAULT 0,
    model             VARCHAR(50) NOT NULL DEFAULT 'gpt-4o-mini',
    created_at        TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_turns_session_created
    ON conversation_turns (session_id, created_at DESC);
"""


async def get_pool() -> asyncpg.Pool:
    global _pool
    if _pool is None:
        _pool = await asyncpg.create_pool(settings.database_url, min_size=1, max_size=5)
    return _pool


async def init_db() -> None:
    pool = await get_pool()
    async with pool.acquire() as conn:
        await conn.execute(DDL)
    logger.info("Database initialized")


async def save_turn(
    session_id: str,
    question: str,
    answer: str,
    context_chunks: list[str],
    usage: dict,
    model: str,
) -> None:
    try:
        pool = await get_pool()
        async with pool.acquire() as conn:
            await conn.execute(
                """
                INSERT INTO conversation_turns
                    (session_id, question, answer, context_chunks,
                     prompt_tokens, completion_tokens, total_tokens, model)
                VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
                """,
                session_id,
                question,
                answer,
                json.dumps(context_chunks),
                usage.get("prompt_tokens", 0),
                usage.get("completion_tokens", 0),
                usage.get("total_tokens", 0),
                model,
            )
    except Exception as exc:
        logger.warning("Failed to persist conversation turn: %s", exc)
