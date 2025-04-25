import streamlit as st
import joblib
import numpy as np
import plotly.graph_objects as go

# Load model
model = joblib.load(r"C:\Users\imash\exercises\project 1\aqi_model.pkl")

st.set_page_config(page_title="AQI Prediction App", layout="centered")

st.markdown("<h1 style='text-align: center; color: #4CAF50;'>🌍 AQI Prediction with Live Meter</h1>", unsafe_allow_html=True)

# Input sliders
features = ['NO2', 'CO', 'SO2', 'O3', 'PM2.5', 'PM10', 'Temperature', 'Humidity']
feature_ranges = {
    'NO2': (0, 300),
    'CO': (0.0, 300.0),
    'SO2': (0, 300),
    'O3': (0, 200),
    'PM2.5': (0, 500),
    'PM10': (0, 500),
    'Temperature': (-10, 50),
    'Humidity': (0, 100)
}

inputs = {}
cols = st.columns(2)
for i, feature in enumerate(features):
    with cols[i % 2]:
        fmin, fmax = feature_ranges[feature]
        inputs[feature] = st.slider(f"{feature}", min_value=float(fmin), max_value=float(fmax), value=float((fmin+fmax)/2), step=0.5)

# Predict button
if st.button("🔍 Predict AQI"):
    input_data = np.array([list(inputs.values())])
    prediction = float(model.predict(input_data)[0])

    # Show Gauge Meter using Plotly
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = prediction,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Predicted AQI"},
        gauge = {
            'axis': {'range': [0, 500]},
            'bar': {'color': "black"},
            'steps': [
                {'range': [0, 50], 'color': "green"},
                {'range': [51, 100], 'color': "yellow"},
                {'range': [101, 150], 'color': "orange"},
                {'range': [151, 200], 'color': "red"},
                {'range': [201, 300], 'color': "purple"},
                {'range': [301, 500], 'color': "maroon"}
            ],
            'threshold': {
                'line': {'color': "black", 'width': 4},
                'thickness': 0.75,
                'value': prediction
            }
        }
    ))

    st.plotly_chart(fig)

    # AQI Category
    def get_category(val):
        if val <= 50:
            return "Good 😊"
        elif val <= 100:
            return "Moderate 🙂"
        elif val <= 150:
            return "Unhealthy for Sensitive 😷"
        elif val <= 200:
            return "Unhealthy 😷"
        elif val <= 300:
            return "Very Unhealthy 😫"
        else:
            return "Hazardous ☠️"

    st.success(f"📈 AQI Category: {get_category(prediction)}")
