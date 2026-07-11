from app.backends.base import RAGBackend
from app.backends.langchain_backend import LangChainRAG
from app.backends.manual_backend import ManualRAG
from app.config import settings


def _create_backend() -> RAGBackend:
    if settings.rag_backend == "langchain":
        return LangChainRAG()

    if settings.rag_backend == "manual":
        return ManualRAG()

    raise ValueError(
        "Unsupported RAG backend: "
        f"{settings.rag_backend}"
    )


# Created once when app.rag is imported
_backend = _create_backend()


def ask_rag(question: str) -> str:
    return _backend.answer(question)