from abc import ABC, abstractmethod


class RAGBackend(ABC):
    @abstractmethod
    def answer(self, question: str) -> str:
        """
        Answer a question using the configured RAG implementation.
        """
        raise NotImplementedError