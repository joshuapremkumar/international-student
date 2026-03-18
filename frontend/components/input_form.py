"""Streamlit degree input form component."""
import streamlit as st


def render_input_form() -> tuple[str, int]:
    """
    Render the degree analysis input form.

    Returns:
        Tuple of (degree: str, top_n: int).
        degree is an empty string if the form was not submitted or input was blank.
    """
    with st.form(key="analyze_form"):
        st.markdown("### 🎓 What degree do you want to study abroad?")
        degree = st.text_input(
            label="Degree",
            placeholder="e.g. Computer Science, MBA, Data Science, Medicine",
            max_chars=200,
            label_visibility="collapsed",
        )
        top_n = st.slider(
            label="Number of countries to compare",
            min_value=3,
            max_value=10,
            value=5,
            step=1,
            help="How many destination countries you want ranked in the results.",
        )
        submitted = st.form_submit_button(
            "🔍 Analyze",
            use_container_width=True,
            type="primary",
        )

    if submitted and degree.strip():
        return degree.strip(), top_n
    return "", top_n
