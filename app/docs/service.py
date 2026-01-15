from __future__ import annotations
from typing import Any, Dict, Iterable, List

from bson import ObjectId

from app.core.config import get_settings
from app.vectorstore.mongo_atlas import get_vector_store


def _docs_to_markdown(docs: Iterable[Any]) -> str:
    lines: list[str] = ["## Tours matching your interest", ""]

    docs_list = list(docs)

    for i, doc in enumerate(docs_list, start=1):
        content = (getattr(doc, "page_content", "") or "").strip()
        if not content:
            content = "(empty document)"

        lines.append(f"{i}. {content}")
        lines.append("")
        # Horizontal rule separator between results.
        if i != len(docs_list):
            lines.extend(["---", ""])

    return "\n".join(lines).strip() + "\n"


def fetch_top_docs_markdown(user_input: str, k: int = 3) -> str:
    """Fetch top-k similar docs and return combined markdown."""

    query = user_input.strip()
    if not query:
        return "## Tours matching your interest\n\n(no query provided)\n"

    vector_store = get_vector_store()
    docs = vector_store.similarity_search(query, k=k)
    return _docs_to_markdown(docs)


def _project_tour_doc(mongo_doc: Dict[str, Any]) -> Dict[str, Any]:
    """Project only the fields that the API should return."""

    allowed = {
        "tour_name",
        "countries",
        "duration_days",
        "price",
        "itinerary_titles",
    }

    projected: Dict[str, Any] = {k: v for k, v in mongo_doc.items() if k in allowed}
    return projected


def fetch_top_docs(user_input: str, k: int = 3) -> List[Dict[str, Any]]:
    """Fetch top-k similar docs and return them as a list of MongoDB documents.

    This uses Atlas Vector Search via `langchain_mongodb`.
    """

    query = user_input.strip()
    if not query:
        return []

    # Only vector search is supported.
    # If the Atlas Search vector index (e.g. `vector_index`) is missing or misconfigured,
    # we raise (no keyword fallback).
    settings = get_settings()
    vector_store = get_vector_store()

    try:
        search_indexes = list(vector_store.collection.list_search_indexes())
    except Exception as exc:  # pragma: no cover
        raise RuntimeError(
            "Unable to verify MongoDB Atlas Search indexes for vector search. "
            "Ensure your MONGODB_URI has permissions to list search indexes."
        ) from exc

    has_vector_index = any(i.get("name") == settings.atlas_vector_index_name for i in search_indexes)
    if not has_vector_index:
        raise RuntimeError(
            f"Atlas Search vector index '{settings.atlas_vector_index_name}' was not found on "
            f"{settings.mongodb_db_name}.{settings.mongodb_collection_name}. "
            "Create the index (MongoDB Atlas > Search) before calling /docs/search."
        )

    docs = vector_store.similarity_search(query, k=k)

    results: List[Dict[str, Any]] = []
    for d in docs:
        mongo_doc: Dict[str, Any] = {}

        metadata = getattr(d, "metadata", None) or {}
        if isinstance(metadata, dict):
            mongo_doc.update(metadata)

        results.append(_project_tour_doc(mongo_doc))

    return results


def fetch_top_docs_structured(user_input: str, k: int = 3) -> Dict[str, Any]:
    query = user_input.strip()
    if not query:
        return {
            "query": query,
            "tours": []
        }

    vector_store = get_vector_store()
    docs = vector_store.similarity_search(query, k=k)

    tours = []
    for d in docs:
        tours.append({
            "tourName": d.metadata.get("tourName"),
            "countries": d.metadata.get("countries", []),
            "source": d.metadata.get("source"),
        })

    return {
        "query": query,
        "tours": tours
    }
