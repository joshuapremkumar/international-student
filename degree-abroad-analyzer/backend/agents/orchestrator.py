"""Orchestrator — coordinates all agents and returns the final AnalysisResult.

Execution flow:
  Phase 1 → Research Agent (Tavily): identifies best candidate countries
  Phase 2 → Visa Agent + Salary Agent (Tavily): parallel fan-out per country
  Phase 3 → ROI Agent (Tinyfish): reasons over merged data, ranks + scores
  Cache  → TTL-based in-memory store to avoid redundant API calls
"""
import asyncio
import logging
from backend.agents import research_agent, visa_agent, salary_agent, roi_agent
from backend.services import cache
from backend.models.response import AnalysisResult
from backend.config import settings

logger = logging.getLogger(__name__)

_DEFAULT_COUNTRIES = [
    "United States", "United Kingdom", "Canada", "Australia", "Germany",
    "Netherlands", "Sweden", "Switzerland", "Singapore", "New Zealand",
    "France", "Ireland", "Denmark", "Norway", "Japan",
]


def _extract_countries(research_data: dict, top_n: int) -> list[str]:
    text = " ".join(
        r.get("content", "") + " " + r.get("title", "")
        for r in research_data.get("raw_results", [])
    ).lower()

    found = []
    seen: set[str] = set()
    for country in _DEFAULT_COUNTRIES:
        if country.lower() in text and country not in seen:
            seen.add(country)
            found.append(country)

    if not found:
        logger.warning("Orchestrator: no countries matched — using default list")
        return _DEFAULT_COUNTRIES[:top_n]

    return found[:top_n]


async def run_analysis(degree: str, top_n: int = 5) -> AnalysisResult:
    """Run the full multi-agent analysis pipeline for a given degree."""
    cached_result = cache.get(degree, top_n)
    if cached_result:
        logger.info("Orchestrator: cache hit for degree='%s' top_n=%d", degree, top_n)
        cached_result.cached = True
        return cached_result

    logger.info("Orchestrator: starting analysis for degree='%s' top_n=%d", degree, top_n)

    # Phase 1: Research
    research_data = await research_agent.research(degree)
    countries = _extract_countries(research_data, top_n)
    logger.info("Orchestrator: selected countries=%s", countries)

    # Phase 2: Visa + Salary (parallel)
    visa_data, salary_data = await asyncio.gather(
        visa_agent.get_visa_info(degree, countries),
        salary_agent.get_salaries(degree, countries),
    )

    # Phase 3: ROI reasoning via Tinyfish
    context = {
        "degree": degree,
        "top_n": top_n,
        "countries": countries,
        "research": research_data["raw_results"],
        "visa": visa_data,
        "salary": salary_data,
    }
    country_results = await roi_agent.compute_roi_and_risk(context)

    result = AnalysisResult(
        degree=degree,
        countries=country_results[:top_n],
        cached=False,
    )

    cache.set(degree, top_n, result, ttl_seconds=settings.CACHE_TTL_SECONDS)
    logger.info("Orchestrator: analysis complete, %d countries returned", len(result.countries))
    return result
