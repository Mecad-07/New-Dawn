import streamlit as st
import pandas as pd
import numpy as np
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from utils.data_loader import load_data


# -------------------------------
# Page Config
# -------------------------------
st.set_page_config(
    page_title="Threat Level Prediction",
    page_icon="🚨",
    layout="wide"
)

# ------------------------------
# Sidebar Styling
# ------------------------------
st.markdown("""
<style>

section[data-testid="stSidebar"] {
    width: 400px !important;
    min-width: 400px !important;
}

section[data-testid="stSidebar"] > div {
    width: 400px !important;
}

section[data-testid="stSidebar"] [data-baseweb="select"] {
    width: 100% !important;
}

section[data-testid="stSidebar"] [data-baseweb="select"] > div {
    min-width: 0 !important;
}

section[data-testid="stSidebar"] [data-baseweb="select"] span {
    white-space: normal !important;
    overflow: visible !important;
    text-overflow: clip !important;
}

div[data-baseweb="popover"] {
    min-width: 380px !important;
}

div[data-baseweb="popover"] li {
    white-space: normal !important;
    word-break: normal !important;
    overflow-wrap: break-word !important;
}

</style>
""", unsafe_allow_html=True)



st.title("🚨 AI Threat Level Prediction System")

# -------------------------------
# Load Dataset
# -------------------------------

df = load_data()

df = df[[
    "country_txt",
    "region_txt",
    "attacktype1_txt",
    "weaptype1_txt",
    "targtype1_txt",
    "nkill",
    "nwound"
]]

df = df.dropna()

# -------------------------------
# Create Threat Level
# -------------------------------
df["impact"] = df["nkill"] + df["nwound"]

def classify_threat(x):
    if x <= 2:
        return "LOW"
    elif x <= 10:
        return "MEDIUM"
    else:
        return "HIGH"

df["threat_level"] = df["impact"].apply(classify_threat)

# -------------------------------
# Encode Categorical Data
encoders = {}

# Keep original text values for the UI
df_ui = df.copy()

# Create separate dataframe for model training
df_encoded = df.copy()

for col in [
    "country_txt",
    "region_txt",
    "attacktype1_txt",
    "weaptype1_txt",
    "targtype1_txt"
]:
    le = LabelEncoder()
    df_encoded[col] = le.fit_transform(df_encoded[col])
    encoders[col] = le

# Encode target
target_encoder = LabelEncoder()
df_encoded["threat_level"] = target_encoder.fit_transform(
    df_encoded["threat_level"]
)

# -------------------------------
# Train Model
# -------------------------------

X = df_encoded.drop(columns=["threat_level", "impact"])
y = df_encoded["threat_level"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42
)

model = RandomForestClassifier(
    n_estimators=200,
    random_state=42
)

model.fit(X_train, y_train)

# ----------------------------
# Session State
# ----------------------------

if "threat_result" not in st.session_state:
    st.session_state.threat_result = None

if "threat_confidence" not in st.session_state:
    st.session_state.threat_confidence = None

if "threat_probability" not in st.session_state:
    st.session_state.threat_probability = None

if "prediction_params" not in st.session_state:
    st.session_state.prediction_params = None
    

# -------------------------------
# Sidebar Inputs
# -------------------------------

st.sidebar.header("Input Parameters")
has_result = st.session_state.threat_result is not None
with st.sidebar.form("threat_prediction_form"):

    # Country
    country = st.selectbox(
        "Country",
        sorted(df_ui["country_txt"].dropna().unique()),
        disabled=has_result
    )

    # Automatically determine region from selected country
    country_data = df_ui[df_ui["country_txt"] == country]

    country_region = (
        country_data["region_txt"]
        .mode()
        .iloc[0]
    )

    # Region is automatically linked to country
    region=st.selectbox(
        "Region",
        [country_region],
        disabled=True
    )

    # Attack Type
    attack = st.selectbox(
        "Attack Type",
        sorted(df_ui["attacktype1_txt"].dropna().unique()),
        disabled=has_result
    )

    # Weapon Type
    weapon = st.selectbox(
        "Weapon Type",
        sorted(df_ui["weaptype1_txt"].dropna().unique()),
        disabled=has_result
    )

    # Target Type
    target = st.selectbox(
        "Target Type",
        sorted(df_ui["targtype1_txt"].dropna().unique()),
        disabled=has_result
    )

    # Number Killed
    nkill = st.number_input(
        "Number Killed",
        min_value=0,
        max_value=1000,
        value=0,
        step=1,
        disabled=has_result
    )

    # Number Wounded
    nwound = st.number_input(
        "Number Wounded",
        min_value=0,
        max_value=1000,
        value=0,
        step=1,
        disabled=has_result
    )

    submitted = st.form_submit_button(
        "🚨 Predict Threat Level",
        disabled=has_result
    )


# ----------------------------
# Prediction
# ----------------------------

if submitted:

    # Encode categorical inputs
    country_encoded = encoders["country_txt"].transform(
        [country]
    )[0]

    region_encoded = encoders["region_txt"].transform(
        [country_region]
    )[0]

    attack_encoded = encoders["attacktype1_txt"].transform(
        [attack]
    )[0]

    weapon_encoded = encoders["weaptype1_txt"].transform(
        [weapon]
    )[0]

    target_encoded = encoders["targtype1_txt"].transform(
        [target]
    )[0]

    # Create model input
    input_data = np.array([[
        country_encoded,
        region_encoded,
        attack_encoded,
        weapon_encoded,
        target_encoded,
        nkill,
        nwound
    ]])

    # Prediction
    prediction = model.predict(input_data)
    probability = model.predict_proba(input_data)

    result = target_encoder.inverse_transform(
        [prediction[0]]
    )[0]

    confidence = np.max(probability) * 100

    # Save result in session state
    st.session_state.threat_result = result
    st.session_state.threat_confidence = confidence
    st.session_state.threat_probability = probability[0]
    st.session_state.prediction_params = {
        "country": country,
        "region": region,
        "attack_type": attack,
        "weapon_type": weapon,
        "target_type": target,
        "nkill": nkill,
        "nwound": nwound
    }
    
    
    st.rerun()

# --------------------------------
# NEW PREDICTION
# --------------------------------

if st.session_state.threat_result is not None:

    if st.sidebar.button(
        "🔄 New Prediction",
        use_container_width=True,
        key="new_prediction_button"
    ):

        st.session_state.threat_result = None
        st.session_state.threat_confidence = None
        st.session_state.threat_probability = None
        st.session_state.prediction_params = None

        st.rerun()

# ----------------------------
# Output
# ----------------------------

if st.session_state.threat_result is not None:

    result = st.session_state.threat_result
    confidence = st.session_state.threat_confidence
    probability = st.session_state.threat_probability

    st.subheader("🔍 Prediction Result")

    if result == "LOW":
        st.success(f"🟢 Threat Level: {result}")

    elif result == "MEDIUM":
        st.warning(f"🟡 Threat Level: {result}")

    else:
        st.error(f"🔴 Threat Level: {result}")

    st.metric(
        "Confidence Score",
        f"{confidence:.2f}%"
    )

    st.write("### Probability Distribution")

    probability_df = pd.DataFrame(
    {
        "Threat Level": target_encoder.classes_,
        "Probability": probability
    }
    ).set_index("Threat Level")

    st.bar_chart(probability_df)


# -----------------------------------------
# Prediction Parameters
# -----------------------------------------
    st.markdown("---")
    st.subheader("📋 Prediction Parameters")

    params = st.session_state.get("prediction_params")

    if params:
        col1, col2 = st.columns(2)

        with col1:
            st.write(f"**Country:** {params['country']}")
            st.write(f"**Region:** {params['region']}")
            st.write(f"**Attack Type:** {params['attack_type']}")
            st.write(f"**Weapon Type:** {params['weapon_type']}")

        with col2:
            st.write(f"**Target Type:** {params['target_type']}")
            st.write(f"**Number Killed:** {params['nkill']}")
            st.write(f"**Number Wounded:** {params['nwound']}")