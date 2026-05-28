import streamlit as st
import requests

st.title("Carshare Prediction")
st.write("Enter details below to get **car_hours** prediction.")

# FastAPI endpoint
# API_URL = "http://127.0.0.1:8000/predict"
import os
API_URL = os.getenv("FASTAPI_URL", "http://localhost:8000") + "/predict"

# Inputs
centroid_lat = st.number_input("Centroid Latitude", value=44.98)
centroid_lon = st.number_input("Centroid Longitude", value=-93.26)
peak_hour = st.number_input("Peak Hour", min_value=0, max_value=23, value=17)

# Predict button
if st.button("Predict"):
    payload = {
        "centroid_lat": centroid_lat,
        "centroid_lon": centroid_lon,
        "peak_hour": peak_hour
    }

    try:
        response = requests.post(API_URL, json=payload)
        result = response.json()

        st.subheader("Predicted Car Hours")
        st.success(result["predicted_car_hours"])

    except Exception as e:
        st.error(f"Error contacting API: {e}")
