"""Tinyfish Agent API service client.

Used exclusively by the ROI Agent for AI reasoning tasks:
  - Country ranking
  - Risk score computation
  - Job demand scoring
  - Salary normalization

Tinyfish exposes an OpenAI-compatible /chat/completions endpoint.
"""
import json
import logging
import httpx
from backend.config import settings

logger = logging.getLogger(__name__)


async def reason(prompt: str, context: dict) -> str:
    """
    Send a system prompt + structured context to Tinyfish and return the response text.

    The context dict is serialized to JSON and sent as the user message.
    The model is expected to return a valid JSON array per the ROI prompt schema.

    Args:
        prompt: System/instruction prompt for the reasoning task.
        context: Structured data dict containing research, visa, and salary info.

    Returns:
        Raw response string from Tinyfish (expected to be a valid JSON array).

    Raises:
        httpx.HTTPStatusError: On non-2xx API response.
        httpx.TimeoutException: On request timeout (90 s).
        ValueError: If response structure is unexpected.
    """
    headers = {
        "Authorization": f"Bearer {settings.TINYFISH_API_KEY}",
        "Content-Type": "application/json",
    }

    # Truncate large search result arrays to stay within token limits
    safe_context = _truncate_context(context, max_chars=12000)

    payload = {
        "model": settings.TINYFISH_MODEL,
        "messages": [
            {"role": "system", "content": prompt},
            {
                "role": "user",
                "content": json.dumps(safe_context, ensure_ascii=False),
            },
        ],
        "temperature": 0.2,
        "max_tokens": 4096,
    }

    logger.info("Calling Tinyfish model=%s", settings.TINYFISH_MODEL)

    async with httpx.AsyncClient(timeout=90.0) as client:
        response = await client.post(
            f"{settings.TINYFISH_BASE_URL}/chat/completions",
            headers=headers,
            json=payload,
        )
        response.raise_for_status()

    data = response.json()

    # Handle both OpenAI-compatible and direct response formats
    if "choices" in data:
        return data["choices"][0]["message"]["content"]
    elif "content" in data:
        return data["content"]
    else:
        raise ValueError(f"Unexpected Tinyfish response structure: {list(data.keys())}")


def _truncate_context(context: dict, max_chars: int = 12000) -> dict:
    """Trim search result content to keep the total payload within token limits."""
    serialized = json.dumps(context, ensure_ascii=False)
    if len(serialized) <= max_chars:
        return context

    trimmed = dict(context)
    for section in ("visa", "salary"):
        if section in trimmed and isinstance(trimmed[section], dict):
            trimmed[section] = {
                country: [
                    {**r, "content": r.get("content", "")[:300]}
                    for r in results[:3]
                ]
                for country, results in trimmed[section].items()
            }
    if "research" in trimmed and isinstance(trimmed["research"], list):
        trimmed["research"] = [
            {**r, "content": r.get("content", "")[:300]}
            for r in trimmed["research"][:5]
        ]
    return trimmed
