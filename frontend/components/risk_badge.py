"""Risk score badge component — color-coded HTML badge by risk level."""


def risk_color(score: float) -> str:
    """Return a hex color based on risk score (lower = safer = greener)."""
    if score <= 3.0:
        return "#2ecc71"   # green  — low risk
    elif score <= 6.0:
        return "#f39c12"   # amber  — moderate risk
    else:
        return "#e74c3c"   # red    — high risk


def risk_label(score: float) -> str:
    """Return a human-readable risk label for a given score."""
    if score <= 3.0:
        return "Low Risk"
    elif score <= 6.0:
        return "Moderate Risk"
    else:
        return "High Risk"


def render_risk_badge(score: float) -> str:
    """
    Return an HTML badge string for the given risk score.

    Args:
        score: Risk score 0.0–10.0.

    Returns:
        Inline HTML string with colored pill badge.
    """
    color = risk_color(score)
    label = risk_label(score)
    return (
        f'<span style="background-color:{color};color:white;padding:4px 12px;'
        f'border-radius:12px;font-size:0.8rem;font-weight:600;">'
        f'⚠️ {label} ({score:.1f}/10)</span>'
    )
