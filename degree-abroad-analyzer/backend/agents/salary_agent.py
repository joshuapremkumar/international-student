"""Salary Agent — salary benchmarks and job demand via Tavily (concurrent fan-out)."""
import asyncio
import logging
from backend.services import tavily_client
from backend.prompts.salary_prompt import build_salary_query

logger = logging.getLogger(__name__)


async def get_salaries(degree: str, countries: list[str]) -> dict:
    """
    Fetch salary benchmarks for each country concurrently.

    Returns:
        Dict mapping country name → list of Tavily result dicts.
    """
    logger.info("Salary Agent: querying %d countries", len(countries))
    coroutines = [
        tavily_client.search(build_salary_query(degree, country), max_results=4)
        for country in countries
    ]
    results = await asyncio.gather(*coroutines, return_exceptions=True)
    salary_data = {}
    for country, result in zip(countries, results):
        if isinstance(result, Exception):
            logger.warning("Salary Agent: failed for '%s': %s", country, result)
            salary_data[country] = []
        else:
            salary_data[country] = result
    return salary_data
