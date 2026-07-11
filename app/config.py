import logging
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

    # Logging
    log_level: str = "INFO"


settings = Settings()


# Configure application logging once, here. This module is imported before the
# backends build, so every module's logger shares one format and level.
# Control verbosity from the environment: LOG_LEVEL=DEBUG in .env to see the
# per-request dumps; default INFO keeps production quiet.
# Keep the ROOT level at WARNING so third-party libraries (urllib3, httpcore,
# anthropic, sentence_transformers, ...) stay quiet by default. Setting the root
# to DEBUG would turn on DEBUG for EVERY library and flood the logs.
logging.basicConfig(
    level=logging.WARNING,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
)

# Raise ONLY our own application logger ("app" and its children) to the
# configured level — so LOG_LEVEL controls OUR verbosity, not the libraries'.
logging.getLogger("app").setLevel(settings.log_level.upper())
