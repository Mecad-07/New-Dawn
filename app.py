import streamlit as st
from config.settings import *
from utils.data_loader import load_data

def load_css():

    with open("assets/styles.css") as f:

        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True
        )

load_css()

st.set_page_config(
    page_title=APP_NAME,
    page_icon=APP_ICON,
    layout=LAYOUT,
    initial_sidebar_state=INITIAL_SIDEBAR_STATE
)
# ==========================
# Sidebar
# ==========================

# ==============================
# Sidebar
# ==============================

st.sidebar.image(
    "https://img.icons8.com/fluency/96/shield.png",
    width=70
)

st.sidebar.title("🛡️ Military Intelligence")
st.sidebar.caption("AI Threat Intelligence Dashboard")
st.sidebar.caption("Version 2.0")

st.sidebar.markdown("---")

st.sidebar.markdown("""
### 🧭 Navigation

Select a module from the sidebar to explore
the intelligence dashboard.
""")

st.sidebar.markdown("---")

st.sidebar.success("🟢 System Status: Ready")

st.sidebar.info("📊 Dataset: Global Terrorism Database")

st.sidebar.markdown("""
**🤖 Machine Learning**  
Random Forest

**📈 Forecasting**  
Linear Regression
""")

st.sidebar.markdown("---")

st.sidebar.caption("© 2026 AI Military Intelligence Dashboard")


# Load dataset
df = load_data()
st.title(APP_TITLE)

st.markdown("## 📊 Dashboard Summary")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(
        f'<div class="metric-card"><div class="metric-title">🌐 Total Incidents</div><div class="metric-value">{len(df):,}</div><div class="metric-sub">Global Terrorism Database</div></div>',
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        f'<div class="metric-card"><div class="metric-title">🌍 Countries</div><div class="metric-value">{df["country_txt"].nunique():,}</div><div class="metric-sub">Countries Covered</div></div>',
        unsafe_allow_html=True
    )


with col3:
    st.markdown(
        f'<div class="metric-card"><div class="metric-title">☠️ Total Fatalities</div><div class="metric-value">{int(df["nkill"].sum()):,}</div><div class="metric-sub">Recorded Fatalities</div></div>',
        unsafe_allow_html=True
    )

with col4:
    st.markdown(
        f'<div class="metric-card"><div class="metric-title">🤕 Total Injuries</div><div class="metric-value">{int(df["nwound"].sum()):,}</div><div class="metric-sub">Recorded Injuries</div></div>',
        unsafe_allow_html=True
    )

# --------------------------------------------------
# Welcome
# --------------------------------------------------

st.markdown("""
## 👋 Welcome to the AI Threat Intelligence Dashboard

This dashboard provides interactive analysis, visualization,
prediction and forecasting using the **Global Terrorism Database (GTD)**.

Use the modules in the sidebar to explore historical terrorism
patterns, analyze countries and attacks, assess threat levels,
and generate data-driven insights.
""")

st.markdown("## 🧭 Available Modules")

module_col1, module_col2 = st.columns(2)

with module_col1:
    st.markdown("""
    **🌍 Global Threat Map**  
    Visualize terrorism incidents across different geographical regions.

    **🌐 Country Analysis**  
    Analyze terrorism activity and patterns for individual countries.

    **🎯 Attack Prediction**  
    Predict the likely attack type based on selected incident parameters.

    **🚨 Threat Level Prediction**  
    Estimate the threat level as **Low, Medium, or High**.
    """)

with module_col2:
    st.markdown("""
    **📈 Forecasting**  
    Forecast future terrorism attack trends using historical data.

    **🧠 AI Intelligence Report**  
    Generate analytical summaries and insights from the dataset.

    **📊 Data Explorer**  
    Filter, inspect, visualize and download the GTD dataset.

    **🛡️ Risk Analysis**  
    Identify countries and patterns associated with higher risk.
    """)

st.markdown("---")

st.info("""
### ℹ️ About This System

This project is developed for **academic and analytical purposes**.
The predictions and forecasts are statistical estimates based on
historical data and should not be considered definitive real-world
threat assessments.
""")

