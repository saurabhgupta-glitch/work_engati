from __future__ import annotations

from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application configuration loaded from environment variables.

    NOTE: We intentionally keep this small and explicit to avoid
    hidden configuration.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    mongodb_uri: str = Field(alias="MONGODB_URI")

    # MongoDB Atlas Vector Search details
    mongodb_db_name: str = "travellive_db"
    mongodb_collection_name: str = "tour_departure_package"
    atlas_vector_index_name: str = "vector_index"
    text_key: str = "content"
    embedding_key: str = "embedding"

    # Embeddings model (OpenAI)
    # Ref: https://platform.openai.com/docs/guides/embeddings
    embeddings_model_name: str = "text-embedding-ada-002"


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Cached settings instance."""

    return Settings()
