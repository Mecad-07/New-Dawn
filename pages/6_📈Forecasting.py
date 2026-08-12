import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

from sklearn.linear_model import LinearRegression
from utils.data_loader import load_data


# ----------------------------------------------------
# Page Configuration
# ----------------------------------------------------
st.set_page_config(
    page_title="Forecasting",
    page_icon="📈",
    layout="wide"
)

st.title("📈 Terrorism Attack Forecasting")

st.markdown("""
Forecast the future number of terrorist attacks using historical GTD data.
""")

# ----------------------------------------------------
# Load Dataset
# ----------------------------------------------------

df = load_data()

# ----------------------------------------------------
# Sidebar Filters
# ----------------------------------------------------
st.sidebar.header("Forecast Settings")

countries = sorted(df["country_txt"].dropna().unique())

country = st.sidebar.selectbox(
    "Select Country",
    countries
)

forecast_years = st.sidebar.slider(
    "Forecast Years",
    1,
    10,
    5
)

# ----------------------------------------------------
# Prepare Data
# ----------------------------------------------------
country_df = df[df["country_txt"] == country]

yearly = (
    country_df
    .groupby("iyear")
    .size()
    .reset_index(name="Attacks")
    .rename(columns={"iyear": "year"})
)

yearly["year"] = pd.to_numeric(yearly["year"], errors="coerce")
yearly["Attacks"] = pd.to_numeric(yearly["Attacks"], errors="coerce")

yearly = yearly.dropna(subset=["year", "Attacks"])
yearly["year"] = yearly["year"].astype(int)
yearly["Attacks"] = yearly["Attacks"].astype(int)

yearly = yearly.sort_values("year").reset_index(drop=True)

# ----------------------------------------------------
# Check data availability
# ----------------------------------------------------
if len(yearly) < 5:
    st.warning("Not enough historical data for forecasting.")
    st.stop()

# ============================
# Forecast Model Back-Testing
# ============================

st.markdown("---")
st.subheader("🧪 Forecast Model Validation")

# Use the latest historical year as a test point
if len(yearly) >= 6:

    train_data = yearly.iloc[:-1]
    test_data = yearly.iloc[-1:]

    X_train = train_data[["year"]]
    y_train = np.log1p(train_data["Attacks"])

    X_test = test_data[["year"]]
    y_test = test_data["Attacks"]

    validation_model = LinearRegression()
    validation_model.fit(X_train, y_train)

    log_prediction = validation_model.predict(X_test)

    test_prediction = np.expm1(log_prediction)
    test_prediction = np.maximum(test_prediction, 0)

    actual_value = float(y_test.iloc[0])
    predicted_value = float(test_prediction[0])

    if actual_value > 0:
        validation_error = (
            abs(predicted_value - actual_value)
            / actual_value
        ) * 100
    else:
        validation_error = 0

    validation_col1, validation_col2, validation_col3 = st.columns(3)

    with validation_col1:
        st.metric(
            "Actual Attacks",
            f"{actual_value:.0f}"
        )

    with validation_col2:
        st.metric(
            "Predicted Attacks",
            f"{predicted_value:.0f}"
        )

    with validation_col3:
        st.metric(
            "Prediction Error",
            f"{validation_error:.1f}%"
        )

    if validation_error <= 20:
        validation_status = "🟢 Good historical fit"

    elif validation_error <= 40:
        validation_status = "🟡 Moderate historical fit"

    else:
        validation_status = "🔴 High historical error"

    st.info(
        f"Validation result: **{validation_status}**"
    )

    # Add a caution when percentage error is very high
    if validation_error > 100:
        if actual_value <= 5:
            st.warning(
                "⚠️ Caution: The latest historical attack count is very low, "
                "so the percentage error is unusually high. "
                "The forecast should be interpreted with caution."
            )
        else:
            st.warning(
                "⚠️ Caution: The historical prediction error is very high. "
                "Forecast results should be interpreted with caution."
            )

# ---------------------------------------------------
# Future Prediction
# ---------------------------------------------------

last_year = int(yearly["year"].max())

future_years = np.arange(
    last_year + 1,
    last_year + forecast_years + 1
)


# Use the most recent 10 years to capture the current trend
forecast_history = yearly.tail(min(10, len(yearly)))

# Apply log transformation to stabilize the attack counts
X = forecast_history[["year"]]
y = np.log1p(forecast_history["Attacks"])

model = LinearRegression()
model.fit(X, y)

future_years = np.arange(
    last_year + 1,
    last_year + forecast_years + 1
)

log_predictions = model.predict(
    pd.DataFrame({"year": future_years})
)

# Convert predictions back to original attack-count scale
predictions = np.expm1(log_predictions)

# Ensure attack counts are non-negative
predictions = np.maximum(predictions, 0)

# Round to whole attacks
predictions = np.round(predictions).astype(int)

# Check for very low or zero forecast values
low_forecast_warning = np.any(predictions <= 1)

# Convert predictions to integers
forecast = pd.DataFrame({
    "Year": future_years,
    "Forecasted Attacks": np.rint(predictions).astype(int)
})

# ----------------------------------------------------
# Historical + Forecast Plot
# ----------------------------------------------------
fig = go.Figure()

fig.add_trace(
    go.Scatter(
        x=yearly["year"],
        y=yearly["Attacks"],
        mode="lines+markers",
        name="Historical"
    )
)

fig.add_trace(
    go.Scatter(
        x=forecast["Year"],
        y=forecast["Forecasted Attacks"],
        mode="lines+markers",
        name="Forecast"
    )
)

fig.update_layout(
    title=f"Attack Forecast for {country}",
    xaxis_title="Year",
    yaxis_title="Number of Attacks",
    height=600
)

st.plotly_chart(fig, use_container_width=True)

# ----------------------------------------------------
# Forecast Table
# ----------------------------------------------------
st.subheader("Forecast Results")

st.dataframe(
    forecast,
    use_container_width=True
)

if low_forecast_warning:
    st.warning(
        "⚠️ Caution: The forecast contains very low or zero attack counts. "
        "This reflects the historical trend used by the model and should not "
        "be interpreted as certainty that no attacks will occur."
    )
# ----------------------------------------------------
# Growth Analysis
# ----------------------------------------------------
historical_last = yearly.iloc[-1]["Attacks"]
forecast_last = forecast.iloc[-1]["Forecasted Attacks"]

growth = (
    (forecast_last - historical_last)
    / max(historical_last, 1)
) * 100

st.subheader("Growth Analysis")

col1, col2, col3 = st.columns(3)

col1.metric(
    "Current Attacks",
    int(historical_last)
)

col2.metric(
    f"Forecast ({forecast_years} Years)",
    int(forecast_last)
)

col3.metric(
    "Growth %",
    f"{growth:.2f}%"
)

# ----------------------------------------------------
# Risk Assessment
# ----------------------------------------------------
st.subheader("Risk Assessment")

if growth < 0:
    st.success("🟢 Threat Trend: Decreasing")
elif growth < 15:
    st.warning("🟡 Threat Trend: Stable")
else:
    st.error("🔴 Threat Trend: Increasing")

# ----------------------------------------------------
# Download Forecast
# ----------------------------------------------------
csv = forecast.to_csv(index=False)

st.download_button(
    label="📥 Download Forecast CSV",
    data=csv,
    file_name=f"{country}_forecast.csv",
    mime="text/csv"
)