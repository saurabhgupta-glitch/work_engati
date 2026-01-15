from __future__ import annotations

from pydantic import BaseModel, Field


class DocSearchRequest(BaseModel):
    user_input: str = Field(..., min_length=1, description="User query text")


class DocSearchResponse(BaseModel):
    markdown: str = Field(..., description="Combined Markdown of the top matching docs")

