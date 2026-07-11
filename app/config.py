from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

    # Secret
    anthropic_api_key: str = Field(
        validation_alias="ANTHROPIC_API_KEY"
    )

    # LLM
    llm_model: str = "claude-haiku-4-5"
    max_tokens: int = 200

    # Embeddings
    embedding_model: str = (
        "sentence-transformers/all-MiniLM-L6-v2"
    )

    # Chunking
    chunk_size: int = 300
    chunk_overlap: int = 50

    # Retrieval
    top_k: int = 2

    # Backend selector
    rag_backend: Literal["langchain", "manual"] = "langchain"


settings = Settings()