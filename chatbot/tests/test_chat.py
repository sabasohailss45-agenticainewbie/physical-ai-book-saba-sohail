"""Tests for POST /api/chat endpoint."""
import pytest
from unittest.mock import AsyncMock, patch
from httpx import AsyncClient, ASGITransport
from uuid import uuid4

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app.main import app

SESSION_ID = str(uuid4())
FAKE_EMBEDDING = [0.1] * 1536


@pytest.mark.asyncio
async def test_chat_question_too_long_returns_422():
    payload = {"question": "x" * 2001, "session_id": SESSION_ID}
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post("/api/chat", json=payload)
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_chat_missing_session_id_returns_422():
    payload = {"question": "What is a humanoid robot?"}
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post("/api/chat", json=payload)
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_chat_happy_path_returns_answer():
    fake_chunks = [
        {
            "chunk_id": "foundations-intro_0",
            "chapter_slug": "foundations-intro",
            "module_id": "foundations",
            "content": "Physical AI refers to AI systems that are embodied in a physical form...",
            "score": 0.95,
        }
    ]
    with (
        patch("app.routes.chat.embed_text", new=AsyncMock(return_value=FAKE_EMBEDDING)),
        patch("app.routes.chat.retrieve_chunks", new=AsyncMock(return_value=fake_chunks)),
        patch("app.routes.chat.generate_answer", new=AsyncMock(return_value=("A humanoid robot is...", {}))),
        patch("app.routes.chat.save_turn", new=AsyncMock()),
    ):
        payload = {"question": "What is a humanoid robot?", "session_id": SESSION_ID}
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            response = await client.post("/api/chat", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
    assert data["answer"] == "A humanoid robot is..."
    assert "request_id" in data


@pytest.mark.asyncio
async def test_chat_out_of_scope_returns_polite_message():
    """When Qdrant returns no chunks, chatbot returns out-of-scope message."""
    with (
        patch("app.routes.chat.embed_text", new=AsyncMock(return_value=FAKE_EMBEDDING)),
        patch("app.routes.chat.retrieve_chunks", new=AsyncMock(return_value=[])),
        patch(
            "app.routes.chat.generate_answer",
            new=AsyncMock(return_value=("This topic is not covered in the current textbook modules.", {})),
        ),
        patch("app.routes.chat.save_turn", new=AsyncMock()),
    ):
        payload = {"question": "What is the stock price of Tesla?", "session_id": SESSION_ID}
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            response = await client.post("/api/chat", json=payload)

    assert response.status_code == 200
    assert "not covered" in response.json()["answer"].lower()
