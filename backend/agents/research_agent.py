"""Research Agent — best countries and job demand via Tavily."""
import logging
from backend.services import tavily_client
from backend.prompts.research_prompt import build_research_query

logger = logging.getLogger(__name__)


async def research(degree: str) -> dict:
    """
    Run a Tavily search for the best countries to study the given degree abroad.

    Returns:
        Dict with keys:
          - degree (str)
          - raw_results (list[dict]): title, url, content, score
    """
    query = build_research_query(degree)
    logger.info("Research Agent: querying Tavily for degree='%s'", degree)
    results = await tavily_client.search(query, max_results=7)
    logger.info("Research Agent: received %d results", len(results))
    return {"degree": degree, "raw_results": results}
