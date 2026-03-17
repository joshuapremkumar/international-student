"""Pydantic request models."""
from pydantic import BaseModel, Field


class AnalyzeRequest(BaseModel):
    """Request payload for degree analysis."""
    degree: str = Field(
        ...,
        min_length=2,
        max_length=200,
        examples=["Computer Science"],
        description="The degree the user wants to study abroad.",
    )
    top_n: int = Field(
        default=5,
        ge=1,
        le=10,
        description="Number of countries to return (1-10).",
    )
