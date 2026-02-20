import logging
from openai import AsyncOpenAI
from app.config import settings

logger = logging.getLogger(__name__)
_client: AsyncOpenAI | None = None


def _get_client() -> AsyncOpenAI:
    global _client
    if _client is None:
        _client = AsyncOpenAI(api_key=settings.openai_api_key)
    return _client


async def embed_text(text: str) -> list[float]:
    """Generate an embedding vector for the given text."""
    try:
        client = _get_client()
        response = await client.embeddings.create(
            model=settings.openai_embedding_model,
            input=text,
        )
        return response.data[0].embedding
    except Exception as exc:
        logger.error("OpenAI embedding failed: %s", exc)
        raise
