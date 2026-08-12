import streamlit as st
import plotly.express as px
from utils.data_loader import load_data


# --------------------------------------------------
# Page Configuration
# --------------------------------------------------

st.set_page_config(
    page_title="Global Threat Map",
    page_icon="🌍",
    layout="wide"
)


# --------------------------------------------------
# Load Dataset
# --------------------------------------------------

df = load_data()


# --------------------------------------------------
# Page Header
# --------------------------------------------------

st.title("🌍 Global Threat Map")

st.markdown("""
Explore the geographical distribution of terrorism incidents
using historical data from the **Global Terrorism Database (GTD)**.
Use the sidebar to filter the map by year.
""")


# --------------------------------------------------
# Sidebar Filters
# --------------------------------------------------

st.sidebar.header("🎛️ Map Filters")

year = st.sidebar.selectbox(
    "Select Year",
    ["All"] + sorted(df["iyear"].dropna().unique().tolist())
)

if year != "All":
    df = df[df["iyear"] == year]


# --------------------------------------------------
# Dataset Summary
# --------------------------------------------------

st.markdown("### 📊 Map Summary")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Incidents",
        f"{len(df):,}"
    )

with col2:
    st.metric(
        "Countries",
        f"{df['country_txt'].nunique():,}"
    )

with col3:
    st.metric(
        "Fatalities",
        f"{int(df['nkill'].fillna(0).sum()):,}"
    )

with col4:
    st.metric(
        "Injuries",
        f"{int(df['nwound'].fillna(0).sum()):,}"
    )


# --------------------------------------------------
# Prepare Map Data
# --------------------------------------------------

map_df = df.dropna(subset=["latitude", "longitude"])


# --------------------------------------------------
# Global Threat Map
# --------------------------------------------------

st.markdown("### 🗺️ Terrorism Incident Distribution")

if len(map_df) == 0:

    st.warning("No geographical data is available for the selected filter.")

else:

    fig = px.scatter_geo(
        map_df,
        lat="latitude",
        lon="longitude",
        color="attacktype1_txt",
        hover_name="country_txt",
        hover_data={
            "city": True,
            "gname": True,
            "nkill": True,
            "latitude": False,
            "longitude": False
        },
        projection="natural earth"
    )

    fig.update_layout(
        height=650,
        margin=dict(l=0, r=0, t=20, b=0),
        legend_title_text="Attack Type"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# --------------------------------------------------
# Information
# --------------------------------------------------

st.info(
    "💡 Use the **Select Year** filter in the sidebar to explore "
    "terrorism incidents for a specific year."
)