"""Visa Agent — post-study work visa data via Tavily (concurrent fan-out)."""
import asyncio
import logging
from backend.services import tavily_client
from backend.prompts.visa_prompt import build_visa_query

logger = logging.getLogger(__name__)


async def get_visa_info(degree: str, countries: list[str]) -> dict:
    """
    Fetch post-study work visa details for each country concurrently.

    Returns:
        Dict mapping country name → list of Tavily result dicts.
    """
    logger.info("Visa Agent: querying %d countries", len(countries))
    coroutines = [
        tavily_client.search(build_visa_query(degree, country), max_results=4)
        for country in countries
    ]
    results = await asyncio.gather(*coroutines, return_exceptions=True)
    visa_data = {}
    for country, result in zip(countries, results):
        if isinstance(result, Exception):
            logger.warning("Visa Agent: failed for '%s': %s", country, result)
            visa_data[country] = []
        else:
            visa_data[country] = result
    return visa_data
