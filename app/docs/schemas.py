from __future__ import annotations

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field
from pydantic import RootModel


class DocSearchRequest(BaseModel):
    user_input: str = Field(..., min_length=1, description="User query text")


class TourPackageDoc(BaseModel):
    tour_name: Optional[str] = None
    countries: List[str] = []
    duration_days: Optional[int] = None
    price: Optional[float] = None
    itinerary_titles: List[str] = []


class DocSearchResponse(RootModel[List[TourPackageDoc]]):
    """Response for `/docs/search`.

    A JSON list of the top matching MongoDB documents (sanitized), not markdown.
    """
    pass


# Used by the `/search-tours` endpoint in `main.py`
class SearchToursRequest(BaseModel):
    query: str = Field(..., min_length=1, description="User search query")
    k: int = Field(3, ge=1, le=10, description="Number of results")
