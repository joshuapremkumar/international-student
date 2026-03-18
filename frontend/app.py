"""Streamlit frontend — Degree Abroad Analyzer.

Entry point for the UI. Renders the input form, calls the FastAPI backend,
and displays ranked country results with job demand, salary, visa, and risk data.
"""
import os
import sys
import logging
import streamlit as st
import httpx

# Ensure project root is on the path so frontend/backend imports resolve
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from frontend.api_client import analyze_degree, BACKEND_URL
from frontend.components.input_form import render_input_form
from frontend.components.country_card import render_country_card

# ── Logging ────────────────────────────────────────────────────────────
LOG_DIR = os.path.join(PROJECT_ROOT, "logs")
os.makedirs(LOG_DIR, exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(os.path.join(LOG_DIR, "frontend.log")),
    ],
)
logger = logging.getLogger(__name__)

# ── Page config ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Degree Abroad Analyzer",
    page_icon="🌍",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ── Header ──────────────────────────────────────────────────────────────
st.markdown(
    """
    <h1 style='text-align:center;color:#1a1a2e;margin-bottom:4px;'>
        🌍 Degree Abroad Analyzer
    </h1>
    <p style='text-align:center;color:#555;font-size:1.05rem;margin-bottom:30px;'>
        Powered by <strong>Tavily</strong> (web search) + <strong>Tinyfish</strong> (AI reasoning)
    </p>
    """,
    unsafe_allow_html=True,
)

# ── Sidebar ──────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## ⚙️ How It Works")
    st.markdown(
        """
        1. **Research Agent** (Tavily) finds the best countries for your degree
        2. **Visa Agent** (Tavily) looks up post-study work visa rules per country
        3. **Salary Agent** (Tavily) retrieves salary benchmarks per country
        4. **ROI Agent** (Tinyfish AI) synthesizes all data into:
           - Country rankings
           - Job demand scores
           - Salary estimates
           - Visa pathway summaries
           - Risk scores
        """
    )
    st.divider()
    st.markdown(f"**Backend:** `{BACKEND_URL}`")

# ── Input form ──────────────────────────────────────────────────────────────
degree, top_n = render_input_form()

# ── Analysis ──────────────────────────────────────────────────────────────
if degree:
    st.markdown("---")
    with st.spinner(f"🔎 Analyzing **{degree}** across {top_n} countries… this may take 30–60 seconds."):
        try:
            result = analyze_degree(degree=degree, top_n=top_n)
        except httpx.ConnectError:
            st.error(
                f"❌ Cannot connect to the backend at `{BACKEND_URL}`. "
                "Make sure the FastAPI server is running."
            )
            st.stop()
        except httpx.HTTPStatusError as exc:
            detail = exc.response.json().get("detail", str(exc))
            st.error(f"❌ Backend error ({exc.response.status_code}): {detail}")
            st.stop()
        except httpx.TimeoutException:
            st.error(
                "⏱️ The analysis timed out. The AI pipeline may be under load — "
                "please try again in a moment."
            )
            st.stop()
        except Exception as exc:
            st.error(f"❌ Unexpected error: {exc}")
            st.stop()

    countries = result.get("countries", [])
    cached = result.get("cached", False)
    generated_at = result.get("generated_at", "")

    st.markdown(f"## 📊 Results for **{result.get('degree', degree)}**")

    col1, col2, col3 = st.columns(3)
    col1.metric("Countries Analyzed", len(countries))
    col2.metric(
        "Best Country",
        next((c["country"] for c in countries if c.get("rank") == 1), "—"),
    )
    col3.metric(
        "Lowest Risk",
        next(
            (c["country"] for c in sorted(countries, key=lambda x: x.get("risk_score", 99))),
            "—",
        ),
    )

    if cached:
        st.info("⚡ Result served from cache.")

    st.markdown("---")

    if countries:
        sorted_countries = sorted(countries, key=lambda x: x.get("rank", 99))
        for i, country in enumerate(sorted_countries):
            render_country_card(country, i)
    else:
        st.warning("No country results returned. Please try a different degree.")

    if countries:
        st.markdown("---")
        st.markdown("### 💰 Salary Comparison (USD/year)")
        chart_data = {
            c["country"]: c.get("average_salary_usd", 0)
            for c in sorted(countries, key=lambda x: x.get("rank", 99))
        }
        import pandas as pd
        df = pd.DataFrame(
            list(chart_data.items()), columns=["Country", "Avg Salary (USD)"]
        ).set_index("Country")
        st.bar_chart(df)

        st.markdown("### ⚠️ Risk Score Summary")
        risk_data = [
            {
                "Rank": c.get("rank"),
                "Country": c.get("country"),
                "Job Demand": f"{c.get('job_demand_score', 0):.1f}/10",
                "Avg Salary (USD)": f"${c.get('average_salary_usd', 0):,}",
                "Visa Difficulty": c.get("visa_difficulty", "N/A"),
                "Risk Score": f"{c.get('risk_score', 0):.1f}/10",
            }
            for c in sorted(countries, key=lambda x: x.get("rank", 99))
        ]
        st.dataframe(risk_data, use_container_width=True, hide_index=True)

    if generated_at:
        st.caption(f"Generated at: {generated_at}")
