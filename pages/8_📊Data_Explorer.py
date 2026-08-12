import streamlit as st
import pandas as pd
import plotly.express as px
from utils.data_loader import load_data
# --------------------------------------------------------
# Page Configuration
# --------------------------------------------------------

st.set_page_config(
    page_title="Data Explorer",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Global Terrorism Data Explorer")

st.markdown("Explore, filter, visualize and download the GTD dataset.")

# --------------------------------------------------------
# Load Dataset
# --------------------------------------------------------
df = load_data()


# -----------------------------
# Sidebar Filters
# -----------------------------

st.sidebar.header("Filter Dataset")

# Start with complete dataset
filter_base = df.copy()

# -----------------------------
# Year
# -----------------------------

years = sorted(df["iyear"].dropna().unique())

selected_year = st.sidebar.multiselect(
    "Select Year",
    years,
    default=[],
    key="filter_year"
)

if selected_year:
    filter_base = filter_base[
        filter_base["iyear"].isin(selected_year)
    ]


# -----------------------------
# Country
# -----------------------------

countries = sorted(
    filter_base["country_txt"].dropna().unique()
)

selected_country = st.sidebar.multiselect(
    "Select Country",
    countries,
    default=[],
    key="filter_country"
)

if selected_country:
    filter_base = filter_base[
        filter_base["country_txt"].isin(selected_country)
    ]


# -----------------------------
# Region
# -----------------------------

regions = sorted(
    filter_base["region_txt"].dropna().unique()
)

selected_region = st.sidebar.multiselect(
    "Select Region",
    regions,
    default=[],
    key="filter_region"
)

if selected_region:
    filter_base = filter_base[
        filter_base["region_txt"].isin(selected_region)
    ]


# -----------------------------
# Attack Type
# -----------------------------

attack_types = sorted(
    filter_base["attacktype1_txt"].dropna().unique()
)

selected_attack = st.sidebar.multiselect(
    "Attack Type",
    attack_types,
    default=[],
    key="filter_attack"
)

if selected_attack:
    filter_base = filter_base[
        filter_base["attacktype1_txt"].isin(selected_attack)
    ]


# -----------------------------
# Weapon Type
# -----------------------------

weapons = sorted(
    filter_base["weaptype1_txt"].dropna().unique()
)

selected_weapon = st.sidebar.multiselect(
    "Weapon Type",
    weapons,
    default=[],
    key="filter_weapon"
)

if selected_weapon:
    filter_base = filter_base[
        filter_base["weaptype1_txt"].isin(selected_weapon)
    ]


# -----------------------------
# Terrorist Group
# -----------------------------

groups = sorted(
    filter_base["gname"].dropna().unique()
)

selected_group = st.sidebar.multiselect(
    "Terrorist Group",
    groups,
    default=[],
    key="filter_group"
)

if selected_group:
    filter_base = filter_base[
        filter_base["gname"].isin(selected_group)
    ]

# -----------------------------
# Final Filtered Dataset
# -----------------------------
filtered_df = filter_base.copy()


# --------------------------------------------------------
# Search Box
# --------------------------------------------------------

search = st.text_input(
    "🔍 Search by City or Country"
)

if search:

    filtered_df = filtered_df[
        filtered_df["city"].fillna("").str.contains(
            search,
            case=False
        )
        |
        filtered_df["country_txt"].fillna("").str.contains(
            search,
            case=False
        )
    ]

# ---------------------------------------------------------
# Check Filter Results
# ---------------------------------------------------------

if filtered_df.empty:
    st.warning(
        "⚠️ No incidents match the selected filters. "
        "Please remove one or more filters and try again."
    )
    st.stop()

# ---------------------------------------------------------
# KPIs
# ---------------------------------------------------------

st.subheader("Dataset Summary")

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Incidents",
    len(filtered_df)
)

c2.metric(
    "Countries",
    filtered_df["country_txt"].nunique()
)

c3.metric(
    "Fatalities",
    int(filtered_df["nkill"].fillna(0).sum())
)

c4.metric(
    "Injuries",
    int(filtered_df["nwound"].fillna(0).sum())
)

# --------------------------------------------------------
# Dataset Preview
# --------------------------------------------------------

st.subheader("Filtered Dataset")

display_columns = [
    "eventid",
    "iyear",
    "imonth",
    "iday",
    "country_txt",
    "region_txt",
    "city",
    "attacktype1_txt",
    "targtype1_txt",
    "weaptype1_txt",
    "gname",
    "nkill",
    "nwound"
]

available_columns = [
    col for col in display_columns
    if col in filtered_df.columns
]

display_df = filtered_df[available_columns].copy()

display_df = display_df.rename(columns={
    "eventid": "Event ID",
    "iyear": "Year",
    "imonth": "Month",
    "iday": "Day",
    "country_txt": "Country",
    "region_txt": "Region",
    "city": "City",
    "attacktype1_txt": "Attack Type",
    "targtype1_txt": "Target Type",
    "weaptype1_txt": "Weapon Type",
    "gname": "Terrorist Group",
    "nkill": "Fatalities",
    "nwound": "Injured"
})

st.dataframe(
    display_df,
    use_container_width=True,
    height=500,
    hide_index=True
)

# --------------------------------------------------------
# Download CSV
# --------------------------------------------------------

csv = filtered_df.to_csv(index=False)

st.download_button(
    "📥 Download Filtered Data",
    csv,
    file_name="Filtered_GTD_Data.csv",
    mime="text/csv"
)

# --------------------------------------------------------
# Charts
# --------------------------------------------------------

st.subheader("Visual Analytics")

tab1, tab2, tab3 = st.tabs([
    "Country",
    "Attack Type",
    "Weapon Type"
])

# ---------------- Country ----------------

with tab1:

    country_chart = (
        filtered_df["country_txt"]
        .value_counts()
        .head(10)
        .reset_index()
    )

    country_chart.columns = [
        "Country",
        "Incidents"
    ]

    fig = px.bar(
        country_chart,
        x="Country",
        y="Incidents",
        color="Incidents",
        title="Top 10 Countries"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# ---------------- Attack ----------------

with tab2:

    attack_chart = (
        filtered_df["attacktype1_txt"]
        .value_counts()
        .reset_index()
    )

    attack_chart.columns = [
        "Attack Type",
        "Count"
    ]

    fig = px.pie(
        attack_chart,
        names="Attack Type",
        values="Count",
        title="Attack Type Distribution"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# ---------------- Weapon ----------------

with tab3:

    weapon_chart = (
        filtered_df["weaptype1_txt"]
        .value_counts()
        .reset_index()
    )

    weapon_chart.columns = [
        "Weapon",
        "Count"
    ]

    fig = px.bar(
        weapon_chart,
        x="Weapon",
        y="Count",
        color="Count",
        title="Weapon Type Distribution"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# ---------------------------------------------------------
# Missing Values
# ---------------------------------------------------------

st.subheader("Missing Values")

missing = (
    filtered_df.isnull()
    .sum()
    .sort_values(ascending=False)
)

# Keep only columns that have missing values
missing = missing[missing > 0]

missing = missing.reset_index()

missing.columns = [
    "Column Name",
    "Missing Values"
]

# Calculate missing percentage
if len(filtered_df) > 0:
    missing["Missing %"] = (
        missing["Missing Values"]
        / len(filtered_df)
        * 100
    ).round(2)
else:
    missing["Missing %"] = 0


# Keep only columns that have some missing values,
# but are not completely empty
missing = missing[
    (missing["Missing Values"] > 0)
    &
    (missing["Missing Values"] < len(filtered_df))
]

# Sort highest missing values first
missing = missing.sort_values(
    "Missing Values",
    ascending=False
)

# Rename common columns
missing["Column Name"] = missing["Column Name"].replace({
    "eventid": "Event ID",
    "iyear": "Year",
    "imonth": "Month",
    "iday": "Day",
    "country_txt": "Country",
    "region_txt": "Region",
    "city": "City",
    "attacktype1_txt": "Attack Type",
    "targtype1_txt": "Target Type",
    "weaptype1_txt": "Weapon Type",
    "gname": "Terrorist Group",
    "nkill": "Fatalities",
    "nwound": "Injured"
})


if missing.empty:
    st.success(
        "✅ No partially missing values found in the selected dataset."
    )
else:
    st.dataframe(
        missing,
        use_container_width=True,
        hide_index=True
    )

# --------------------------------------------------------
# Dataset Information
# --------------------------------------------------------

st.subheader("Dataset Information")

info1, info2, info3 = st.columns(3)

info1.metric(
    "Rows",
    filtered_df.shape[0]
)

info2.metric(
    "Columns",
    filtered_df.shape[1]
)

info3.metric(
    "Memory Usage",
    f"{filtered_df.memory_usage(deep=True).sum() / 1024**2:.2f} MB"
)

st.write("Available Columns")

st.dataframe(
    pd.DataFrame({
        "Column Name": filtered_df.columns
    }).reset_index(drop=True),
    use_container_width=True,
    height=300,
    hide_index=True
)
st.caption(
    f"The filtered dataset contains {filtered_df.shape[1]} columns."
)