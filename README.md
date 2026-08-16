# AI Powered Terrorism Intelligence Dashboard

## Overview

This project was developed as part of an internship to explore threat intelligence, data analysis, visualization, forecasting, and machine-learning-based security analysis.

The application uses historical Global Terrorism Database (GTD) data and provides an interactive dashboard for exploring terrorism-related patterns, trends, threat levels, attack prediction, and risk analysis.

## Objectives

- Analyze historical terrorism-related data.
- Visualize global and country-level threat patterns.
- Identify trends and important characteristics of reported incidents.
- Provide machine-learning-based attack prediction.
- Perform threat-level and risk analysis.
- Provide historical trend forecasting.
- Present complex data through an interactive and user-friendly dashboard.

## Key Modules

### 1. Home Dashboard
Provides an overview of the application and access to the different analytical modules.

### 2. Global Threat Map
Visualizes the geographical distribution of historical terrorism incidents.

### 3. Country Analysis
Provides detailed country-level statistics, trends, attack types, organizations, weapons, and incident information.

### 4. Attack Prediction
Uses a trained machine-learning classification model to predict the attack category based on selected incident-related features.

### 5. Threat Level
Provides a risk-oriented assessment based on available historical and analytical information.

### 6. Forecasting
Analyzes historical trends and provides a baseline forecast using Linear Regression.

### 7. AI Intelligence
Provides a summarized intelligence-oriented view of important indicators and patterns in the dataset.

### 8. Data Explorer
Allows users to explore and filter the underlying terrorism dataset.

### 9. Risk Analysis
Provides country-level risk assessment, risk drivers, historical comparisons, and early-warning indicators.

## Machine Learning

The Attack Prediction module uses a trained classification model based on historical terrorism data.

The dataset was cleaned and processed, followed by feature encoding and model training.

The evaluated model achieved approximately **85.5% accuracy on the test dataset**.

This result represents model performance on the evaluated dataset and should not be interpreted as a guarantee of real-world events.

## Dataset

The project uses historical data from the **Global Terrorism Database (GTD)**.

The dataset contains information related to terrorism incidents, including geographical information, attack characteristics, targets, weapons, casualties, and other incident-related attributes.

## Technologies Used

- Python
- Streamlit
- Pandas
- Scikit-learn
- Joblib
- Data Visualization
- Machine Learning

## Project Structure

```text
├── app.py
├── assets/
├── config/
├── data/
├── intelligence/
├── models/
├── pages/
├── utils/
├── train_attack_model.py
├── check_gtd.py
├── merge_gtd.py
├── requirements.txt
├── .gitignore
└── .gitattributes
