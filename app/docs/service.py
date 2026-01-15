from __future__ import annotations

from typing import Any, Dict, Iterable

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
