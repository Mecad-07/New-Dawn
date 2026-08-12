import streamlit as st
import plotly.graph_objects as go
import pandas as pd

from utils.data_loader import load_data
from intelligence.risk_engine import (
    calculate_risk_score,
    get_risk_factors,
    get_risk_level
)

st.set_page_config(page_title="Threat Risk Analysis", layout="wide")

st.title("🛡️ Threat Risk Analysis")

df = load_data()

countries = sorted(df["country_txt"].dropna().unique())

country = st.selectbox(
    "Select Country",
    countries
)
# Filter selected country
country_df = df[df["country_txt"] == country]

# Basic Statistics
total_incidents = len(country_df)
total_killed = int(country_df["nkill"].sum())
total_wounded = int(country_df["nwound"].sum())

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Total Incidents",
        f"{total_incidents:,}"
    )

with col2:
    st.metric(
        "Total Fatalities",
        f"{total_killed:,}"
    )

with col3:
    st.metric(
        "Total Injuries",
        f"{total_wounded:,}"
    )



st.markdown("---")

st.caption(
    "Overall score from 0–100 based on incident frequency, fatality severity, recent activity, and attack success."
)

# ============================
# Recent Activity Trend
# ============================

st.markdown("---")

st.subheader("📈 Recent Activity Trend")
yearly_attacks = (
    country_df
    .groupby("iyear")
    .size()
    .reset_index(name="Attacks")
)

latest_year = int(yearly_attacks["iyear"].max())
recent_start = latest_year - 9

# Include years with zero recorded attacks
recent_years = pd.DataFrame({
    "iyear": range(recent_start, latest_year + 1)
})

recent_attacks = recent_years.merge(
    yearly_attacks,
    on="iyear",
    how="left"
)

recent_attacks["Attacks"] = (
    recent_attacks["Attacks"]
    .fillna(0)
    .astype(int)
)

fig_trend = go.Figure()

fig_trend.add_trace(
    go.Scatter(
        x=recent_attacks["iyear"],
        y=recent_attacks["Attacks"],
        mode="lines+markers",
        name="Attacks"
    )
)

fig_trend.update_layout(
    xaxis_title="Year",
    yaxis_title="Number of Attacks",
    hovermode="x unified"
)

st.plotly_chart(
    fig_trend,
    use_container_width=True
)

if len(recent_attacks) >= 2:

    first_year_attacks = recent_attacks.iloc[0]["Attacks"]
    last_year_attacks = recent_attacks.iloc[-1]["Attacks"]

    if first_year_attacks > 0:
        trend_change = (
            (last_year_attacks - first_year_attacks)
            / first_year_attacks
        ) * 100
    elif last_year_attacks > 0:
        trend_change = 100
else:
    trend_change = 0


if trend_change > 20:
    trend_status = "🔴 Strongly Increasing"

elif trend_change > 5:
    trend_status = "🟠 Increasing"

elif trend_change < -20:
    trend_status = "🟢 Strongly Decreasing"

elif trend_change < -5:
    trend_status = "🟢 Decreasing"

else:
    trend_status = "🟡 Relatively Stable"

st.metric(
    "10-Year Activity Change",
    f"{trend_change:+.1f}%"
)

st.info(
    f"10-year activity trend: **{trend_status}**"
)

# ============================
# Risk Score 2.0
# ============================

# Incident frequency relative to the dataset
country_incident_counts = (
    df.groupby("country_txt")
    .size()
)

max_incidents = country_incident_counts.max()

if max_incidents > 0:
    incident_frequency = (
        total_incidents / max_incidents
    ) * 100
else:
    incident_frequency = 0


# Fatality severity
if total_incidents > 0:
    fatality_rate = total_killed / total_incidents
else:
    fatality_rate = 0

global_fatality_rate = (
    df["nkill"].sum() / len(df)
)

if global_fatality_rate > 0:
    fatality_severity = (
        fatality_rate / global_fatality_rate
    ) * 50
else:
    fatality_severity = 0

fatality_severity = min(fatality_severity, 100)


# Recent activity
recent_activity = min(
    max(50 + trend_change, 0),
    100
)


# Attack success rate
if "success" in country_df.columns:
    success_rate = (
        country_df["success"]
        .dropna()
        .mean()
        * 100
    )
else:
    success_rate = 0


# Calculate final risk score
risk_score = calculate_risk_score(
    incident_frequency,
    fatality_severity,
    recent_activity,
    success_rate
)


# Get individual risk factors
risk_factors = get_risk_factors(
    incident_frequency,
    fatality_severity,
    recent_activity,
    success_rate
)


# Get overall risk level
risk_level = get_risk_level(risk_score)


fig = go.Figure(
    go.Indicator(

        mode="gauge+number",

        value=risk_score,

        title={"text": "Threat Risk Score"},

        gauge={

            "axis": {"range": [0, 100]},

            "bar": {"color": "#1f77b4"},

            "steps": [

                {"range": [0, 35], "color": "#90ee90"},

                {"range": [35, 60], "color": "#ffe066"},

                {"range": [60, 80], "color": "#ffb347"},

                {"range": [80, 100], "color": "#ff6b6b"}

            ]

        }

    )
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.success(f"Threat Level : {risk_level}")

st.markdown("---")

st.subheader("🎯 Risk Drivers")

st.caption(
    "Factors contributing to the overall threat risk score."
)
st.caption(
    "Incident frequency is measured relative to the country with the highest number of incidents in the dataset."
)

driver_col1, driver_col2 = st.columns(2)

with driver_col1:
    st.metric(
        "📊 Incident Frequency",
        f"{incident_frequency:.1f}/100"
    )

    st.progress(
        int(incident_frequency) / 100
    )

    st.metric(
        "💀 Fatality Severity",
        f"{fatality_severity:.1f}/100"
    )

    st.progress(
        int(fatality_severity) / 100
    )

with driver_col2:
    st.metric(
        "📈 Recent Activity",
        f"{recent_activity:.1f}/100"
    )

    st.progress(
        int(recent_activity) / 100
    )

    st.metric(
        "🎯 Attack Success Rate",
        f"{success_rate:.1f}/100"
    )

    st.progress(
        int(success_rate) / 100
    )


# ============================
# Risk Score Composition
# ============================

st.markdown("---")

st.subheader("🧩 Risk Score Composition")

st.caption(
    "Shows the weighted contribution of each factor to the final Threat Risk Score."
)

# Weighted contribution of each factor
incident_contribution = incident_frequency * 0.30
fatality_contribution = fatality_severity * 0.30
recent_contribution = recent_activity * 0.25
success_contribution = success_rate * 0.15

comp_col1, comp_col2, comp_col3, comp_col4 = st.columns(4)

with comp_col1:
    st.metric(
        "📊 Incident Frequency",
        f"+{incident_contribution:.1f}"
    )

with comp_col2:
    st.metric(
        "💀 Fatality Severity",
        f"+{fatality_contribution:.1f}"
    )

with comp_col3:
    st.metric(
        "📈 Recent Activity",
        f"+{recent_contribution:.1f}"
    )

with comp_col4:
    st.metric(
        "🎯 Attack Success",
        f"+{success_contribution:.1f}"
    )

st.info(
    f"🛡️ Combined Risk Score: **{risk_score:.1f}/100**"
)


# Identify the strongest contributing factor
contributions = {
    "Incident Frequency": incident_contribution,
    "Fatality Severity": fatality_contribution,
    "Recent Activity": recent_contribution,
    "Attack Success": success_contribution
}

dominant_factor = max(
    contributions,
    key=contributions.get
)

dominant_value = contributions[dominant_factor]

st.warning(
    f"⚠️ **Primary Risk Driver:** {dominant_factor} "
    f"contributes approximately **{dominant_value:.1f} points** "
    f"to the overall risk score."
)


# ============================
# Historical Risk Baseline
# ============================

st.markdown("---")

st.subheader("📊 Historical Risk Baseline")

st.caption(
    "Compares the recent average attack activity with the country's historical yearly average."
)

# Historical yearly attack counts
historical_yearly = (
    country_df
    .groupby("iyear")
    .size()
    .reset_index(name="Attacks")
    .sort_values("iyear")
)

# Historical average
historical_average = historical_yearly["Attacks"].mean()

# Recent average
recent_average = recent_attacks["Attacks"].mean()

# Compare recent activity with historical baseline
if historical_average > 0:
    baseline_change = (
        (recent_average - historical_average)
        / historical_average
    ) * 100
else:
    baseline_change = 0


baseline_col1, baseline_col2, baseline_col3 = st.columns(3)

with baseline_col1:
    st.metric(
        "📚 Historical Average",
        f"{historical_average:.1f} attacks/year"
    )

with baseline_col2:
    st.metric(
        "📈 Recent Average",
        f"{recent_average:.1f} attacks/year"
    )

with baseline_col3:
    st.metric(
        "📊 Baseline Difference",
        f"{baseline_change:+.1f}%"
    )


    # Interpret the baseline comparison
if baseline_change >= 25:
    baseline_status = "🔴 Significantly Above Historical Baseline"

elif baseline_change >= 10:
    baseline_status = "🟠 Above Historical Baseline"

elif baseline_change <= -25:
    baseline_status = "🟢 Significantly Below Historical Baseline"

elif baseline_change <= -10:
    baseline_status = "🔵 Below Historical Baseline"

else:
    baseline_status = "🟡 Near Historical Baseline"

st.info(
    f"Historical comparison: **{baseline_status}**"
)

baseline_fig = go.Figure()

baseline_fig.add_trace(
    go.Scatter(
        x=historical_yearly["iyear"],
        y=historical_yearly["Attacks"],
        mode="lines+markers",
        name="Yearly Attacks"
    )
)

historical_years = pd.DataFrame({
    "iyear": range(
        int(country_df["iyear"].min()),
        int(country_df["iyear"].max()) + 1
    )
})

historical_complete = historical_years.merge(
    historical_yearly,
    on="iyear",
    how="left"
)

historical_complete["Attacks"] = (
    historical_complete["Attacks"]
    .fillna(0)
    .astype(int)
)

historical_average = historical_complete["Attacks"].mean()

baseline_fig.add_hline(
    y=historical_average,
    line_dash="dash",
    annotation_text="Historical Average"
)

baseline_fig.update_layout(
    title="Country Activity vs Historical Baseline",
    xaxis_title="Year",
    yaxis_title="Number of Attacks",
    hovermode="x unified"
)

st.plotly_chart(
    baseline_fig,
    use_container_width=True
)

# ============================
# Early Warning Signal
# ============================

st.markdown("---")

st.subheader("🚨 Early Warning Signal")

st.caption(
    "Compares average attack activity in the previous 3 years with the most recent 3 years."
)


# Sort yearly activity and include years with zero attacks
early_warning_data = (
    country_df
    .groupby("iyear")
    .size()
    .reset_index(name="Attacks")
    .sort_values("iyear")
)

early_start = int(early_warning_data["iyear"].min())
early_end = int(early_warning_data["iyear"].max())

complete_years = pd.DataFrame({
    "iyear": range(early_start, early_end + 1)
})

early_warning_data = complete_years.merge(
    early_warning_data,
    on="iyear",
    how="left"
)

early_warning_data["Attacks"] = (
    early_warning_data["Attacks"]
    .fillna(0)
    .astype(int)
)

# Need at least 6 consecutive calendar years
if len(early_warning_data) >= 6:

    # Previous 3 calendar years
    previous_period = early_warning_data["Attacks"].iloc[-6:-3].mean()

    # Most recent 3 calendar years
    recent_period = early_warning_data["Attacks"].iloc[-3:].mean()
    if previous_period > 0:
        acceleration_change = (
            (recent_period - previous_period)
            / previous_period
        ) * 100
    else:
        acceleration_change = 0

else:
    previous_period = 0
    recent_period = 0
    acceleration_change = 0

if len(early_warning_data) < 6:

    warning_status = "🟡 Insufficient Historical Data"

elif acceleration_change >= 50:

    warning_status = "🔴 Strong Early Warning"

elif acceleration_change >= 25:

    warning_status = "🟠 Elevated Early Warning"

elif acceleration_change <= -25:

    warning_status = "🟢 Activity Declining"

else:

    warning_status = "🔵 No Significant Acceleration"


warning_col1, warning_col2, warning_col3 = st.columns(3)

with warning_col1:
    st.metric(
        "Previous 3-Year Average",
        f"{previous_period:.1f}"
    )

with warning_col2:
    st.metric(
        "Recent 3-Year Average",
        f"{recent_period:.1f}"
    )

with warning_col3:
    st.metric(
        "Activity Change",
        f"{acceleration_change:+.1f}%"
    )

st.info(
    f"Early warning assessment: **{warning_status}**"
)

warning_fig = go.Figure()

warning_fig.add_trace(
    go.Bar(
        x=["Previous 3 Years", "Recent 3 Years"],
        y=[previous_period, recent_period],
        name="Average Attacks"
    )
)

warning_fig.update_layout(
    title="Previous vs Recent Activity",
    xaxis_title="Period",
    yaxis_title="Average Attacks per Year",
    showlegend=False
)

st.plotly_chart(
    warning_fig,
    use_container_width=True
)

