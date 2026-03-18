import json
import logging
import httpx
from backend.config import settings

logger = logging.getLogger(__name__)


async def reason(prompt: str, context: dict) -> str:

    headers = {
        "X-API-Key": settings.TINYFISH_API_KEY,
        "Content-Type": "application/json",
    }

    payload = {
        "url": "https://example.com",
        "goal": f"{prompt}\n\nDATA:\n{json.dumps(context)}"
    }

    logger.info("Calling Tinyfish Automation API")

    async with httpx.AsyncClient(timeout=90.0) as client:
        response = await client.post(
            "https://agent.tinyfish.ai/v1/automation/run",
            headers=headers,
            json=payload,
        )

    if response.status_code != 200:
        logger.error("Tinyfish response error: %s", response.text)
        response.raise_for_status()

    data = response.json()

    if "output" in data:
        return data["output"]

    if "result" in data:
        return data["result"]

    return json.dumps(data)