"""ROI Agent — risk scoring and country ranking via Tinyfish AI reasoning."""
import json
import logging
from backend.services import tinyfish_client
from backend.prompts.roi_prompt import ROI_SYSTEM_PROMPT
from backend.models.response import CountryResult

logger = logging.getLogger(__name__)


async def compute_roi_and_risk(context: dict) -> list[CountryResult]:
    """
    Use Tinyfish to reason over merged agent context and return ranked CountryResult list.

    Raises:
        ValueError: If Tinyfish response cannot be parsed as valid JSON array.
    """
    logger.info(
        "ROI Agent: calling Tinyfish for degree='%s', countries=%s",
        context.get("degree"),
        context.get("countries"),
    )

    raw_response = await tinyfish_client.reason(
        prompt=ROI_SYSTEM_PROMPT,
        context=context,
    )

    logger.debug("ROI Agent: raw Tinyfish response: %s", raw_response[:500])

    # Strip markdown code fences if the model wrapped the JSON
    cleaned = raw_response.strip()
    if cleaned.startswith("```"):
        lines = cleaned.split("\n")
        lines = lines[1:]
        if lines and lines[-1].strip().startswith("```"):
            lines = lines[:-1]
        cleaned = "\n".join(lines).strip()

    try:
        data = json.loads(cleaned)
    except json.JSONDecodeError as exc:
        raise ValueError(
            f"ROI Agent: Tinyfish returned invalid JSON.\n"
            f"Parse error: {exc}\n"
            f"Raw response (first 1000 chars): {raw_response[:1000]}"
        ) from exc

    if not isinstance(data, list):
        raise ValueError(
            f"ROI Agent: Expected a JSON array, got {type(data).__name__}. "
            f"Response: {raw_response[:500]}"
        )

    logger.info("ROI Agent: parsed %d country results", len(data))
    return [CountryResult(**item) for item in data]
