def calculate_risk_score(
    incident_frequency,
    fatality_severity,
    recent_activity,
    success_rate
):
    """
    Calculates an explainable threat risk score (0-100).
    """

    score = (
        incident_frequency * 0.30
        + fatality_severity * 0.30
        + recent_activity * 0.25
        + success_rate * 0.15
    )

    return round(min(max(score, 0), 100), 2)


def get_risk_factors(
    incident_frequency,
    fatality_severity,
    recent_activity,
    success_rate
):
    """
    Returns the individual factors used to calculate risk.
    """

    return {
        "Incident Frequency": round(incident_frequency, 2),
        "Fatality Severity": round(fatality_severity, 2),
        "Recent Activity": round(recent_activity, 2),
        "Attack Success": round(success_rate, 2)
    }

def get_risk_level(score):

    if score >= 85:
        return "🔴 Critical"

    elif score >= 65:
        return "🟠 High"

    elif score >= 40:
        return "🟡 Medium"

    else:
        return "🟢 Low"

    