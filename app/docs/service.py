from __future__ import annotations

from typing import Iterable

from typing import Any

from app.vectorstore.mongo_atlas import get_vector_store


def _docs_to_markdown(docs: Iterable[Any]) -> str:
    lines: list[str] = ["## Tours matching your interest", ""]

    for i, doc in enumerate(docs, start=1):
        content = (getattr(doc, "page_content", "") or "").strip()
        if not content:
            content = "(empty document)"

        lines.append(f"{i}. {content}")
        lines.append("")
        # Horizontal rule separator between results.
        if i != 3:
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
