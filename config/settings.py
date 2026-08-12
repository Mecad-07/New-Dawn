"""
Global configuration for the AI Military Intelligence Dashboard
"""

# ==============================
# Dashboard Information
# ==============================

APP_NAME = "AI Military Intelligence Dashboard"
APP_ICON = "🛡️"
APP_TITLE = "AI-Powered Terrorism Intelligence Dashboard"

LAYOUT = "wide"
INITIAL_SIDEBAR_STATE = "expanded"

# ==============================
# Theme Colors
# ==============================

PRIMARY_COLOR = "#1f77b4"
SUCCESS_COLOR = "#28a745"
WARNING_COLOR = "#ffc107"
DANGER_COLOR = "#dc3545"

# ==============================
# Dataset
# ==============================

DATASET_PATH = "data/globalterrorism.csv"

# ==============================
# Models
# ==============================

MODEL_FOLDER = "models"

ATTACK_MODEL = "models/attack_prediction_model.pkl"
FEATURE_ENCODER = "models/feature_encoders.pkl"
TARGET_ENCODER = "models/target_encoder.pkl"

# ==============================
# Map
# ==============================

DEFAULT_MAP_ZOOM = 2
DEFAULT_MAP_STYLE = "OpenStreetMap"

# ==============================
# Forecast
# ==============================

DEFAULT_FORECAST_YEARS = 5