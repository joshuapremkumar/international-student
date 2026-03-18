"""Pydantic response models."""
from datetime import datetime
from pydantic import BaseModel, Field


class CountryResult(BaseModel):
    """Analysis result for a single country."""
    country: str = Field(..., description="Country name")
    rank: int = Field(..., description="Rank among returned countries (1 = best)")
    job_demand_score: float = Field(
        ..., ge=0.0, le=10.0, description="Job demand score 0-10 (higher = more demand)"
    )
    average_salary_usd: int = Field(
        ..., description="Average annual salary in USD for the given degree"
    )
    post_study_visa: str = Field(
        ..., description="Visa name and duration (e.g. 'Graduate Route Visa – 2 years')"
    )
    visa_difficulty: str = Field(
        ..., description="Visa application difficulty: Easy | Moderate | Hard"
    )
    risk_score: float = Field(
        ..., ge=0.0, le=10.0, description="Risk score 0-10 (lower = safer/better)"
    )
    summary: str = Field(
        ..., description="2-sentence narrative summary for this country"
    )


class AnalysisResult(BaseModel):
    """Top-level response returned by /api/v1/analyze."""
    degree: str = Field(..., description="The degree that was analyzed")
    countries: list[CountryResult] = Field(
        ..., description="Ranked list of country results"
    )
    generated_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="UTC timestamp when the analysis was generated",
    )
    cached: bool = Field(
        default=False, description="True if this result was served from the in-memory cache"
    )
