"""Application configuration loaded from environment variables."""
import os
from dotenv import load_dotenv

# Load .env from the project root
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", ".env"))


class Settings:
    # Tavily — web search for research, visa, salary agents
    TAVILY_API_KEY: str = os.getenv("TAVILY_API_KEY", "")

    # Tinyfish — AI reasoning for ROI agent
    TINYFISH_API_KEY: str = os.getenv("TINYFISH_API_KEY", "")
    TINYFISH_BASE_URL: str = os.getenv("TINYFISH_BASE_URL", "https://api.tinyfish.ai/v1")
    TINYFISH_MODEL: str = os.getenv("TINYFISH_MODEL", "tinyfish")

    # Backend server
    BACKEND_HOST: str = os.getenv("BACKEND_HOST", "0.0.0.0")
    BACKEND_PORT: int = int(os.getenv("BACKEND_PORT", "8000"))

    # TTL cache (seconds)
    CACHE_TTL_SECONDS: int = int(os.getenv("CACHE_TTL_SECONDS", "3600"))


settings = Settings()
