import logging

from app.backends.base import RAGBackend
from app.config import settings
from functools import lru_cache

logger = logging.getLogger(__name__)


def _create_backend() -> RAGBackend:
    logger.info("Creating RAG backend: %s", settings.rag_backend)

    if settings.rag_backend == "langchain":
        from app.backends.langchain_backend import LangChainRAG
        return LangChainRAG()

    if settings.rag_backend == "manual":
        from app.backends.manual_backend import ManualRAG
        return ManualRAG()

    logger.error("Unsupported RAG backend: %s", settings.rag_backend)
    raise ValueError(
        "Unsupported RAG backend: "
        f"{settings.rag_backend}"
    )

@lru_cache
def get_backend() -> RAGBackend:
    # Lazy + cached: built on first call, then reused. Importing this module
    # no longer builds the pipeline — so tests that override it pay nothing.
    return _create_backend()