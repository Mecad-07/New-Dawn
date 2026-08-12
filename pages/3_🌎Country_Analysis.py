import streamlit as st
import plotly.express as px
from utils.data_loader import load_data

st.set_page_config(
    page_title="Country Analysis",
    page_icon="🌎",
    layout="wide"
)

st.title("🌐 Country Intelligence Analysis")
st.markdown("Detailed analysis of terrorism incidents, attack patterns, organizations and locations.")

df = load_data()

# Sidebar
# ------------------------------

st.sidebar.header("Country Filters")

countries = sorted(df["country_txt"].dropna().unique())

country = st.sidebar.selectbox(
    "Select Country",
    countries
)
country_df = df[df["country_txt"] == country]

st.header(f"📊 Intelligence Report: {country}")
st.caption(f"Analysis of terrorism incidents recorded for {country}.")

# ------------------------------
# Key Statistics
# ------------------------------

st.subheader("📈 Key Statistics")

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Incidents",
    f"{len(country_df):,}"
)

c2.metric(
    "Fatalities",
    int(country_df["nkill"].sum())
)

c3.metric(
    "Injured",
    int(country_df["nwound"].sum())
)

c4.metric(
    "Groups",
    country_df["gname"].nunique()
)

st.divider()

# -----------------------------
# Attacks Over Time
# -----------------------------

left, right = st.columns(2)

with left:

    yearly = (
        country_df
        .groupby("iyear")
        .size()
        .reset_index(name="Attacks")
    )

    fig = px.line(
    yearly,
    x="iyear",
    y="Attacks",
    markers=True,
    title="Attacks Over Years",
    labels={
        "iyear": "Year",
        "Attacks": "Number of Attacks"
        }
    )

    fig.update_traces(
        hovertemplate="Year: %{x}<br>Attacks: %{y}<extra></extra>"
    )

    fig.update_layout(
        height=450,
        autosize=True,
        margin=dict(l=60, r=20, t=60, b=50),
        xaxis=dict(
            title="Year",
            dtick=5
        ),
        yaxis=dict(
            title="Number of Attacks",
            rangemode="tozero"
        )
    )

    fig.update_layout(
    autosize=True,
    height=450,
    margin=dict(l=20, r=20, t=60, b=40)
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        config={
            "responsive": True,
            "displayModeBar": True
            }
    )

with right:

    attack = (
        country_df
        .groupby("attacktype1_txt")
        .size()
        .reset_index(name="Count")
    )

    fig = px.pie(
    attack,
    names="attacktype1_txt",
    values="Count",
    title="Attack Types",
    hole=0.35,
    labels={
        "attacktype1_txt": "Attack Type",
        "Count": "Number of Attacks"
        }
    )

    fig.update_traces(
        textposition="inside",
        textinfo="percent",
        hovertemplate=(
            "Attack Type: %{label}<br>"
            "Number of Attacks: %{value}<br>"
            "Percentage: %{percent}<extra></extra>"
        )
    )

    fig.update_layout(
        height=450,
        autosize=True,
        margin=dict(l=20, r=20, t=60, b=40)
    )


    st.plotly_chart(
        fig,
        use_container_width=True
    )

st.divider()

# -----------------------------
# Organizations
# -----------------------------

left, right = st.columns(2)

with left:

    groups = (
        country_df
        .groupby("gname")
        .size()
        .reset_index(name="Attacks")
        .sort_values("Attacks", ascending=False)
        .head(10)
    )

    fig = px.bar(
        groups,
        x="Attacks",
        y="gname",
        orientation="h",
        title="Top Terrorist Organizations",
        labels={
            "gname": "Organization",
            "Attacks": "Number of Attacks"
        },
        text="Attacks"
    )

    fig.update_traces(
        textposition="outside",
        hovertemplate=(
            "Organization: %{y}<br>"
            "Number of Attacks: %{x}<extra></extra>"
        )
    )

    fig.update_layout(
        height=450,
        autosize=True,
        margin=dict(l=20, r=80, t=60, b=40),
        yaxis=dict(
            title="Organization",
            automargin=True
        ),
        xaxis=dict(
            title="Number of Attacks",
            rangemode="tozero"
        )
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


with right:

    weapon = (
        country_df
        .groupby("weaptype1_txt")
        .size()
        .reset_index(name="Count")
        .sort_values("Count", ascending=False)
    )

    fig = px.bar(
        weapon,
        x="Count",
        y="weaptype1_txt",
        orientation="h",
        title="Weapon Types",
        labels={
            "weaptype1_txt": "Weapon Type",
            "Count": "Number of Attacks"
        },
        text="Count"
    )

    fig.update_traces(
        textposition="outside",
        hovertemplate=(
            "Weapon Type: %{y}<br>"
            "Number of Attacks: %{x}<extra></extra>"
        )
    )

    fig.update_layout(
        height=450,
        autosize=True,
        margin=dict(l=20, r=80, t=60, b=40),
        yaxis=dict(
            title="Weapon Type",
            automargin=True,
            tickfont=dict(size=10)
        ),
        xaxis=dict(
            title="Number of Attacks",
            rangemode="tozero"
        )
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


st.divider()

# -----------------------------
# Incident Map
# -----------------------------

st.subheader("Incident Locations")

map_df = country_df.dropna(
    subset=["latitude", "longitude"]
).copy()

# Clean display names for map hover
map_df["Country"] = map_df["country_txt"]
map_df["Year"] = map_df["iyear"]
map_df["Attack Type"] = map_df["attacktype1_txt"]
map_df["Organization"] = map_df["gname"]
map_df["Killed"] = map_df["nkill"]

fig = px.scatter_geo(
    map_df,
    lat="latitude",
    lon="longitude",
    hover_name="city",
    hover_data={
        "Country": True,
        "Year": True,
        "Attack Type": True,
        "Organization": True,
        "Killed": True,
        "latitude": False,
        "longitude": False
    },
    color="attacktype1_txt",
    labels={
        "attacktype1_txt": "Attack Type"
    },
    projection="natural earth",
    title=f"Terrorist Incidents in {country}",
    height=500
)

fig.update_layout(
    margin=dict(l=0, r=0, t=50, b=0),
    legend_title_text="Attack Type"
)

st.plotly_chart(
    fig,
    use_container_width=True,
    key="country_incident_map"
)


st.divider()

# -----------------------------
# Incident Table
# -----------------------------

st.subheader("Incident Details")
#clean and rename columns for display
incident_table = country_df[
    [
        "iyear",
        "city",
        "attacktype1_txt",
        "targtype1_txt",
        "weaptype1_txt",
        "gname",
        "nkill",
        "nwound"
    ]

].rename(columns={
    "iyear": "Year",
    "city": "City",
    "attacktype1_txt": "Attack Type",
    "targtype1_txt": "Target Type",
    "weaptype1_txt": "Weapon Type",
    "gname": "Organization",
    "nkill": "Killed",
    "nwound": "Wounded"
})

st.dataframe(
    incident_table,
    use_container_width=True,
    hide_index=True,
    height=500
)
# -----------------------------
# Download
# -----------------------------

csv = country_df.to_csv(
    index=False
).encode("utf-8")

st.download_button(
    "📥Download Country Data",
    csv,
    file_name=f"{country}_data.csv",
    mime="text/csv",
    use_container_width=True
)