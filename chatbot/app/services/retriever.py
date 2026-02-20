import logging
from qdrant_client import AsyncQdrantClient
from qdrant_client.models import SearchRequest
from app.config import settings

logger = logging.getLogger(__name__)
_client: AsyncQdrantClient | None = None


def _get_client() -> AsyncQdrantClient:
    global _client
    if _client is None:
        _client = AsyncQdrantClient(
            url=settings.qdrant_url,
            api_key=settings.qdrant_api_key,
        )
    return _client


async def retrieve_chunks(embedding: list[float], top_k: int = 5) -> list[dict]:
    """Search Qdrant for the top_k most similar chunks."""
    try:
        client = _get_client()
        results = await client.search(
            collection_name=settings.qdrant_collection,
            query_vector=embedding,
            limit=top_k,
            with_payload=True,
        )
        chunks = []
        for hit in results:
            payload = hit.payload or {}
            chunks.append({
                "chunk_id": payload.get("chunk_id", ""),
                "chapter_slug": payload.get("chapter_slug", ""),
                "module_id": payload.get("module_id", ""),
                "content": payload.get("content", ""),
                "score": hit.score,
            })
        return chunks
    except Exception as exc:
        logger.error("Qdrant search failed: %s", exc)
        return []
