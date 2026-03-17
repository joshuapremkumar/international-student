"""Search query builder for the Visa Agent (Tavily)."""


def build_visa_query(degree: str, country: str) -> str:
    """
    Build a Tavily search query for post-study work visa rules.

    Args:
        degree: The degree the user wants to study abroad.
        country: The destination country.

    Returns:
        Optimized search query string.
    """
    return (
        f"Post-study work visa {country} for international {degree} graduates 2024 2025: "
        f"visa name, duration, eligibility requirements, application process, "
        f"renewal options, pathway to permanent residency, job search visa"
    )
