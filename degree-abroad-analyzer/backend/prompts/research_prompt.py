"""Search query builder for the Research Agent (Tavily)."""


def build_research_query(degree: str) -> str:
    """
    Build an advanced Tavily search query for best countries and job demand.

    Args:
        degree: The degree the user wants to study abroad.

    Returns:
        Optimized search query string.
    """
    return (
        f"Best countries to study {degree} abroad 2024 2025: "
        f"job market demand, employment rate, top hiring industries, "
        f"graduate employment outcomes, international student opportunities, "
        f"university rankings, tuition fees, quality of life"
    )
