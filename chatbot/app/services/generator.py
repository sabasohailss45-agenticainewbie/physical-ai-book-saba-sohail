import logging
from openai import AsyncOpenAI
from app.config import settings

logger = logging.getLogger(__name__)
_client: AsyncOpenAI | None = None

SYSTEM_PROMPT = """You are an expert tutor for the Physical AI & Humanoid Robotics textbook.
Answer ONLY based on the provided context from the textbook.
If the answer is not found in the context, respond:
"This topic is not covered in the current textbook modules. Try asking about Physical AI foundations, sensing, actuation, or humanoid robots."

Be concise, accurate, and educational. Use bullet points or numbered lists when listing items.

Context:
{context}"""

OUT_OF_SCOPE_RESPONSE = (
    "This topic is not covered in the current textbook modules. "
    "Try asking about Physical AI foundations, sensing & perception, "
    "actuation & control, or humanoid robot architecture."
)


def _get_client() -> AsyncOpenAI:
    global _client
    if _client is None:
        _client = AsyncOpenAI(api_key=settings.openai_api_key)
    return _client


async def generate_answer(
    question: str,
    chunks: list[dict],
) -> tuple[str, dict]:
    """Generate an answer using retrieved chunks as context."""
    if not chunks:
        return OUT_OF_SCOPE_RESPONSE, {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}

    context = "\n\n---\n\n".join(
        f"[{c['chapter_slug']}]\n{c['content']}" for c in chunks
    )
    system_message = SYSTEM_PROMPT.format(context=context)

    try:
        client = _get_client()
        response = await client.chat.completions.create(
            model=settings.openai_chat_model,
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": question},
            ],
            temperature=0.3,
            max_tokens=800,
        )
        answer = response.choices[0].message.content or OUT_OF_SCOPE_RESPONSE
        usage = {
            "prompt_tokens": response.usage.prompt_tokens if response.usage else 0,
            "completion_tokens": response.usage.completion_tokens if response.usage else 0,
            "total_tokens": response.usage.total_tokens if response.usage else 0,
        }
        return answer, usage
    except Exception as exc:
        logger.error("OpenAI chat completion failed: %s", exc)
        raise
