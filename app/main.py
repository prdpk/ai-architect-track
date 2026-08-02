import hashlib
import logging
from pathlib import Path

import redis
from fastapi.staticfiles import StaticFiles
from fastapi import Depends, FastAPI

from app.backends.base import RAGBackend
from app.rag import get_backend
from app.schemas import AskRequest, AskResponse
from app.config import settings

logger = logging.getLogger(__name__)

app = FastAPI()

redis_client = redis.Redis(
    host=settings.redis_host,
    port=settings.redis_port,
    decode_responses=True,
)

def _cache_key(question: str) -> str:
    normalized = question.strip().lower()
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()

STATIC_DIR = Path(__file__).resolve().parent / "static"
app.mount("/static", StaticFiles(directory=STATIC_DIR, html=True), name="static")

@app.get("/")
def read_root():
    return {
        "message": "Hello, RAG API"
    }

@app.post("/ask", response_model=AskResponse)
def ask_question(
    request: AskRequest,
    backend: RAGBackend = Depends(get_backend),
) -> AskResponse:
    logger.info("Question: %s", request.question)

    cache_key = _cache_key(request.question)

# Try cache first. Cache failure should never break the API.
    try:
        cached_answer = redis_client.get(cache_key)

        if cached_answer:
            logger.info("Cache hit")
            return AskResponse(answer=cached_answer)

    except Exception as e:
        logger.warning("Redis read failed, continuing without cache: %s", e)

    # Cache miss or Redis unavailable
    result = backend.answer(request.question)
    
    # Store result in cache
    try:
        redis_client.set(
            cache_key,
            result,
            ex=settings.cache_ttl,
        )
        logger.info("Answer cached")

    except Exception as e:
        logger.warning("Redis write failed, returning uncached result: %s", e)

    return AskResponse(answer=result)