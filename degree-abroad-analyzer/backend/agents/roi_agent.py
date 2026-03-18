"""
ROI Agent — local scoring engine replacing Tinyfish.
"""

import logging
from backend.models.response import CountryResult

logger = logging.getLogger(__name__)


def _score_country(country: str, context: dict) -> float:
    salary_data = context.get("salary", {})
    visa_data = context.get("visa", {})

    salary_score = 0
    visa_score = 0

    if country in salary_data and salary_data[country]:
        salary_score = 0.7

    if country in visa_data and visa_data[country]:
        visa_score = 0.3

    return salary_score + visa_score


async def compute_roi_and_risk(context: dict) -> list[CountryResult]:

    degree = context.get("degree")
    countries = context.get("countries", [])

    logger.info("ROI Agent: scoring countries for degree='%s'", degree)

    scored = []

    for country in countries:

        score = _score_country(country, context)

        result = {
            "country": country,
            "rank": 0,  # placeholder

            "roi_score": round(score * 100, 2),
            "risk_score": round((1 - score) * 100, 2),

            "job_demand_score": round(score * 10, 2),

            "average_salary_usd": 70000,

            "post_study_visa": "Available",

            "visa_difficulty": "Medium",

            "summary": f"{country} offers good opportunities for {degree} graduates with moderate visa difficulty and competitive salaries."
        }

        scored.append(result)

    scored.sort(key=lambda x: x["roi_score"], reverse=True)

    results = []

    for rank, item in enumerate(scored, start=1):
        item["rank"] = rank
        results.append(CountryResult(**item))

    logger.info("ROI Agent: ranked %d countries", len(results))

    return results