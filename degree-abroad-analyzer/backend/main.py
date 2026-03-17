"""FastAPI application entrypoint for Degree Abroad Analyzer."""
import logging
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.api.routes.analyze import router as analyze_router
from backend.config import settings

# ── JSON structured logging ─────────────────────────────────────────────
LOG_DIR = os.path.join(os.path.dirname(__file__), "..", "logs")
os.makedirs(LOG_DIR, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(os.path.join(LOG_DIR, "backend.log")),
    ],
)
logger = logging.getLogger(__name__)

# ── FastAPI app ───────────────────────────────────────────────────
app = FastAPI(
    title="Degree Abroad Analyzer",
    description=(
        "Multi-agent AI system that analyzes study-abroad options for any degree.\n\n"
        "**Agents:**\n"
        "- Research Agent (Tavily): best countries + job demand\n"
        "- Visa Agent (Tavily): post-study work visa rules\n"
        "- Salary Agent (Tavily): salary benchmarks\n"
        "- ROI Agent (Tinyfish): risk scoring + country ranking\n"
    ),
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# ── CORS ──────────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Routers ──────────────────────────────────────────────────────────
app.include_router(analyze_router, prefix="/api/v1", tags=["Analysis"])


# ── Health check ─────────────────────────────────────────────────────────
@app.get("/health", tags=["Health"])
async def health_check():
    """Liveness probe — returns service status."""
    return {"status": "ok", "service": "degree-abroad-analyzer"}


@app.on_event("startup")
async def on_startup():
    logger.info(
        "Degree Abroad Analyzer started on %s:%d",
        settings.BACKEND_HOST,
        settings.BACKEND_PORT,
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "backend.main:app",
        host=settings.BACKEND_HOST,
        port=settings.BACKEND_PORT,
        reload=False,
    )
