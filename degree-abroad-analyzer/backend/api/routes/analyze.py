"""POST /api/v1/analyze — degree abroad analysis endpoint."""
import logging
from fastapi import APIRouter, HTTPException
from backend.models.request import AnalyzeRequest
from backend.models.response import AnalysisResult
from backend.agents.orchestrator import run_analysis

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post(
    "/analyze",
    response_model=AnalysisResult,
    summary="Analyze study-abroad options for a degree",
    description=(
        "Accepts a degree name and returns ranked study-abroad country options "
        "with job demand scores, average salaries, post-study visa pathways, "
        "and AI-computed risk scores. Powered by Tavily (search) + Tinyfish (reasoning)."
    ),
)
async def analyze(request: AnalyzeRequest) -> AnalysisResult:
    """
    Run the full multi-agent analysis pipeline and return ranked country results.

    - **degree**: e.g. "Computer Science", "MBA", "Data Science", "Medicine"
    - **top_n**: number of countries to return (1–10, default 5)
    """
    logger.info("POST /analyze — degree='%s' top_n=%d", request.degree, request.top_n)
    try:
        result = await run_analysis(degree=request.degree, top_n=request.top_n)
        return result
    except ValueError as exc:
        logger.error("Validation/parsing error: %s", exc)
        raise HTTPException(status_code=422, detail=str(exc))
    except Exception as exc:
        logger.exception("Agent pipeline error: %s", exc)
        raise HTTPException(
            status_code=502,
            detail=f"Agent pipeline error: {str(exc)}",
        )
