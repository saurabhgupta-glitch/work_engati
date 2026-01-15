from __future__ import annotations

from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv
load_dotenv()

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

    # OpenAI
    # NOTE: Keep the API key in `.env` / environment, not in code.
    openai_api_key: str = Field(alias="OPENAI_API_KEY")

    # MongoDB Atlas Vector Search details
    # NOTE: Updated to the new DB/collection names for tour packages.
    mongodb_db_name: str = "tour_data"
    mongodb_collection_name: str = "tour_package"
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
