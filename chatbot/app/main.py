import logging
import uuid
import time
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from app.config import settings
from app.limiter import limiter
from app.routes import chat

logging.basicConfig(
    level=logging.INFO,
    format='{"level":"%(levelname)s","time":"%(asctime)s","name":"%(name)s","message":"%(message)s"}',
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting Physical AI Textbook Chatbot API")
    yield
    logger.info("Shutting down")


app = FastAPI(
    title="Physical AI Textbook Chatbot API",
    version="1.0.0",
    lifespan=lifespan,
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://physical-ai-book-saba-sohail.vercel.app",
        "https://*.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type", "X-Request-ID"],
)


@app.middleware("http")
async def add_request_id_and_log(request: Request, call_next):
    request_id = str(uuid.uuid4())
    request.state.request_id = request_id
    start = time.monotonic()
    response: Response = await call_next(request)
    latency_ms = round((time.monotonic() - start) * 1000, 1)
    response.headers["X-Request-ID"] = request_id
    logger.info(
        '{"request_id":"%s","method":"%s","path":"%s","status":%d,"latency_ms":%.1f}',
        request_id,
        request.method,
        request.url.path,
        response.status_code,
        latency_ms,
    )
    return response


app.include_router(chat.router, prefix="/api")
