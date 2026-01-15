from __future__ import annotations

from functools import lru_cache

import certifi
from langchain_mongodb import MongoDBAtlasVectorSearch
from langchain_openai import OpenAIEmbeddings
from pymongo import MongoClient

from app.core.config import get_settings


@lru_cache(maxsize=8)
def _get_embeddings(model_name: str) -> OpenAIEmbeddings:
    """Create & cache the OpenAI embeddings model.

    `OPENAI_API_KEY` should be loaded at app startup (see `main.py`).
    """
    return OpenAIEmbeddings(model=model_name)


@lru_cache(maxsize=1)
def get_mongo_client() -> MongoClient:
    settings = get_settings()
    return MongoClient(
        settings.mongodb_uri,
        tls=True,
        tlsCAFile=certifi.where(),
        serverSelectionTimeoutMS=5000,
    )


@lru_cache(maxsize=1)
def get_vector_store() -> MongoDBAtlasVectorSearch:
    """Return a cached MongoDB Atlas Vector Search vector store instance."""

    settings = get_settings()

    client = get_mongo_client()
    db = client[settings.mongodb_db_name]
    collection = db[settings.mongodb_collection_name]

    # If you want a different OpenAI embedding model, set it in Settings.
    embeddings = _get_embeddings(settings.embeddings_model_name)

    return MongoDBAtlasVectorSearch(
        collection=collection,
        embedding=embeddings,
        index_name=settings.atlas_vector_index_name,
        text_key=settings.text_key,
        embedding_key=settings.embedding_key,
    )
