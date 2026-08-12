import streamlit as st
import joblib
import pandas as pd
from utils.data_loader import load_data

model = joblib.load(
    "models/attack_prediction_model.pkl"
)
encoders = joblib.load(
    "models/feature_encoders.pkl"
)
target_encoder = joblib.load(
    "models/target_encoder.pkl"
)


st.set_page_config(
    page_title="Attack Prediction",
    page_icon="🤖",
    layout="wide"
)

if "attack_probabilities" not in st.session_state:
    st.session_state.attack_probabilities = None

if "attack_result" not in st.session_state:
    st.session_state.attack_result = None

if "attack_confidence" not in st.session_state:
    st.session_state.attack_confidence = None

if "attack_prediction_params" not in st.session_state:
    st.session_state.attack_prediction_params = None

st.title("🤖 Attack Type Prediction")

st.markdown("""
Enter the incident details below and click **Predict Attack Type**.
""")

# -------------------------
# Load Dataset
# -------------------------
df = load_data()


# -------------------------
# Remove Missing Values
# -------------------------

df = df.dropna(subset=[
    "country_txt",
    "region_txt",
    "weaptype1_txt",
    "targtype1_txt",
    "gname"
])

# -------------------------
# Create Input Form
# -------------------------

with st.form("prediction_form"):

    col1, col2 = st.columns(2)

    with col1:

        available_countries = sorted(
            set(df["country_txt"].dropna().unique())
            & set(encoders["country_txt"].classes_)
        )

        country = st.selectbox(
            "🌎 Country",
            available_countries
        )

        # Automatically determine the region from the selected country
        country_data = df[df["country_txt"] == country]

        country_region = (
            country_data["region_txt"]
            .mode()
            .iloc[0]
        )

        region = st.selectbox(
            "🌍 Region",
            [country_region],
            disabled=True
        )

        #weapons type
        available_weapons = sorted(
            set(df["weaptype1_txt"].dropna().unique())
            & set(encoders["weaptype1_txt"].classes_)
        )

        weapon = st.selectbox(
            "🔫 Weapon Type",
            available_weapons
        )

        # Target type
        available_targets = sorted(
            set(df["targtype1_txt"].dropna().unique())
            & set(encoders["targtype1_txt"].classes_)
        )

        target = st.selectbox(
            "🎯 Target Type",
            available_targets
        )


    with col2:

        # Show only terrorist groups associated with selected country
        available_groups = sorted(
            set(country_data["gname"].dropna().unique())
            & set(encoders["gname"].classes_)
        )

        group = st.selectbox(
            "👥 Terrorist Group",
            available_groups
        )
        success = st.selectbox(
            "✅ Attack Successful?",
            [0, 1],
            format_func=lambda x: "Yes" if x == 1 else "No"
        )

        suicide = st.selectbox(
            "💣 Suicide Attack?",
            [0, 1],
            format_func=lambda x: "Yes" if x == 1 else "No"
        )

        nkill = st.number_input(
            "☠ Number of Fatalities",
            min_value=0,
            value=0,
            step=1
        )

        nwound = st.number_input(
            "🏥 Number of Injured",
            min_value=0,
            value=0,
            step=1
        )

    submitted = st.form_submit_button("🚀 Predict Attack Type")

    if submitted:
        st.success("Prediction request received.")

        country_encoded = encoders["country_txt"].transform([country])[0]
        region_encoded = encoders["region_txt"].transform([region])[0]
        weapon_encoded = encoders["weaptype1_txt"].transform([weapon])[0]
        target_encoded = encoders["targtype1_txt"].transform([target])[0]
        group_encoded = encoders["gname"].transform([group])[0]

        input_df = pd.DataFrame({
            "country_txt": [country_encoded],
            "region_txt": [region_encoded],
            "weaptype1_txt": [weapon_encoded],
            "targtype1_txt": [target_encoded],
            "gname": [group_encoded],
            "success": [success],
            "suicide": [suicide],
            "nkill": [nkill],
            "nwound": [nwound]
        })

        prediction = model.predict(input_df)
        attack_type = target_encoder.inverse_transform(prediction)[0]
        st.success(f"Predicted Attack Type: {attack_type}")
        probabilities = model.predict_proba(input_df)

        st.session_state.attack_probabilities = probabilities[0]
        confidence = probabilities.max() * 100
        st.session_state.attack_confidence = confidence

        st.session_state.attack_result = attack_type
        st.session_state.attack_prediction_params = {
            "country": country,
            "region": region,
            "weapon_type": weapon,
            "target_type": target,
            "terrorist_group": group,
            "success": success,
            "suicide": suicide,
            "nkill": nkill,
            "nwound": nwound
        }

        st.metric(
            "Prediction Confidence",
            f"{confidence:.2f}%"
        )

        st.divider()

        if st.session_state.attack_result is not None:

            st.subheader("📋 Prediction Parameters")

            params = st.session_state.attack_prediction_params

            col1, col2 = st.columns(2)

            with col1:
                st.write(f"**Country:** {params['country']}")
                st.write(f"**Region:** {params['region']}")
                st.write(f"**Weapon Type:** {params['weapon_type']}")
                st.write(f"**Target Type:** {params['target_type']}")

            with col2:
                st.write(f"**Terrorist Group:** {params['terrorist_group']}")
                st.write(f"**Attack Successful:** {'Yes' if params['success'] == 1 else 'No'}")
                st.write(f"**Suicide Attack:** {'Yes' if params['suicide'] == 1 else 'No'}")
                st.write(f"**Number Killed:** {params['nkill']}")
                st.write(f"**Number Injured:** {params['nwound']}")

            st.divider()

            st.subheader("📊 Prediction Probability")

            probability_df = pd.DataFrame(
                {
                    "Attack Type": target_encoder.classes_,
                    "Probability": st.session_state.attack_probabilities
                }
            ).set_index("Attack Type")

            st.bar_chart(probability_df)
