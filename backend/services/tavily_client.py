"""Tavily API service client.

Used by: Research Agent, Visa Agent, Salary Agent.
Performs advanced web searches and returns synthesized answers + raw results.
"""
import asyncio
from tavily import TavilyClient
from backend.config import settings

# Synchronous Tavily SDK client — wrapped in asyncio for non-blocking calls
_client = TavilyClient(api_key=settings.TAVILY_API_KEY)


async def search(query: str, max_results: int = 5) -> list[dict]:
    """
    Execute a Tavily search and return result list.

    Prepends the synthesized Tavily answer as the first result so agents
    can prioritize it when parsing content.

    Args:
        query: Search query string.
        max_results: Maximum number of web results to return.

    Returns:
        List of dicts with keys: title, url, content, score.
    """
    loop = asyncio.get_event_loop()
    response = await loop.run_in_executor(
        None,
        lambda: _client.search(
            query=query,
            max_results=max_results,
            search_depth="advanced",
            include_answer=True,
        ),
    )

    results: list[dict] = response.get("results", [])
    answer: str = response.get("answer", "")

    if answer:
        results.insert(
            0,
            {
                "title": "Tavily Synthesized Answer",
                "content": answer,
                "url": "",
                "score": 1.0,
            },
        )
    return results
