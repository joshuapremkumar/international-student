"""Search query builder for the Salary Agent (Tavily)."""


def build_salary_query(degree: str, country: str) -> str:
    """
    Build a Tavily search query for salary benchmarks and job demand.

    Args:
        degree: The degree the user wants to study abroad.
        country: The destination country.

    Returns:
        Optimized search query string.
    """
    return (
        f"Average salary {degree} graduate {country} 2024 2025 annual USD: "
        f"entry level salary, mid-level salary, senior salary, "
        f"cost of living adjustment, purchasing power, top paying cities, "
        f"job demand outlook, hiring companies"
    )
