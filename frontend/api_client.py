"""HTTP client for calling the FastAPI /analyze endpoint from the Streamlit frontend."""
import os
import logging
import httpx
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", ".env"))

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

logger = logging.getLogger(__name__)


def analyze_degree(degree: str, top_n: int = 5) -> dict:
    """
    POST to /api/v1/analyze and return the parsed JSON response.

    Args:
        degree: The degree to analyze.
        top_n: Number of countries to return (1–10).

    Returns:
        Parsed AnalysisResult dict.

    Raises:
        httpx.HTTPStatusError: On non-2xx response.
        httpx.ConnectError: If the backend is unreachable.
        httpx.TimeoutException: If the request exceeds the timeout.
    """
    logger.info(
        "api_client: POST %s/api/v1/analyze degree='%s' top_n=%d",
        BACKEND_URL, degree, top_n,
    )
    with httpx.Client(timeout=180.0) as client:
        response = client.post(
            f"{BACKEND_URL}/api/v1/analyze",
            json={"degree": degree, "top_n": top_n},
        )
        response.raise_for_status()
        return response.json()
