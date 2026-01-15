from __future__ import annotations

from fastapi import APIRouter, HTTPException
from pymongo.errors import ServerSelectionTimeoutError

from app.docs.schemas import DocSearchRequest, DocSearchResponse
from app.docs.service import fetch_top_docs


router = APIRouter(prefix="/docs", tags=["docs"])


@router.post("/search", response_model=DocSearchResponse)
def search_docs(payload: DocSearchRequest) -> DocSearchResponse:
    try:
        docs = fetch_top_docs(payload.user_input, k=2)
        return DocSearchResponse(docs)
    except Exception as exc:
        # Don't leak internal stacktraces to clients.
        if isinstance(exc, ServerSelectionTimeoutError):
            raise HTTPException(
                status_code=500,
                detail=(
                    "Failed to connect to MongoDB (ServerSelectionTimeoutError). "
                    "Please verify MONGODB_URI in .env and that your network/IP allowlist "
                    "permits this machine to access the Atlas cluster."
                ),
            ) from exc

        raise HTTPException(
            status_code=500,
            detail=(
                "Failed to fetch documents. "
                "Ensure OPENAI_API_KEY is set in your environment or in .env. "
                f"Error: {exc.__class__.__name__}"
            ),
        ) from exc
