"""Country result card component — renders a styled card for one country."""
import streamlit as st
from frontend.components.risk_badge import render_risk_badge


def render_country_card(country: dict, index: int) -> None:
    """
    Render a single country result as a styled Streamlit card.

    Args:
        country: CountryResult dict from the /analyze API response.
        index: Zero-based position index (for alternating card backgrounds).
    """
    rank = country.get("rank", index + 1)
    name = country.get("country", "Unknown")
    job_score = country.get("job_demand_score", 0.0)
    salary = country.get("average_salary_usd", 0)
    visa = country.get("post_study_visa", "N/A")
    visa_diff = country.get("visa_difficulty", "N/A")
    risk = country.get("risk_score", 5.0)
    summary = country.get("summary", "")

    visa_diff_icons = {"Easy": "🟢", "Moderate": "🟡", "Hard": "🔴"}
    visa_icon = visa_diff_icons.get(visa_diff, "⚪")
    bg_color = "#fafafa" if index % 2 == 0 else "#f0f4ff"

    with st.container():
        st.markdown(
            f"""
            <div style="border:1px solid #dde3ef;border-radius:14px;padding:22px 24px;
                        margin-bottom:18px;background:{bg_color};
                        box-shadow:0 1px 4px rgba(0,0,0,0.06);">
                <h3 style="margin:0 0 6px 0;color:#1a1a2e;">
                    #{rank}&nbsp;&nbsp;🌍 {name}
                </h3>
                <p style="color:#555;margin:0 0 14px 0;font-style:italic;line-height:1.5;">
                    {summary}
                </p>
                <div style="display:flex;flex-wrap:wrap;gap:14px;align-items:center;
                            font-size:0.92rem;">
                    <span>📈 <strong>Job Demand:</strong> {job_score:.1f} / 10</span>
                    <span>💰 <strong>Avg Salary:</strong> ${salary:,} / yr</span>
                    <span>🛂 <strong>Post-Study Visa:</strong> {visa}</span>
                    <span>{visa_icon} <strong>Visa Difficulty:</strong> {visa_diff}</span>
                </div>
                <div style="margin-top:12px;">
                    {render_risk_badge(risk)}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
