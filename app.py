from fastapi import FastAPI
from pydantic import BaseModel
import pickle
import numpy as np

# ----------------------------
# Load model at startup
# ----------------------------
with open("xgb_carshare_model.pkl", "rb") as f:
    model = pickle.load(f)

app = FastAPI(title="Carshare Regression API")


# ----------------------------
# Input Schema
# ----------------------------
class CarshareInput(BaseModel):
    centroid_lat: float
    centroid_lon: float
    peak_hour: float


# ----------------------------
# Root Endpoint
# ----------------------------
@app.get("/")
def home():
    return {"message": "Carshare Prediction API is running"}


# ----------------------------
# Predict Endpoint
# ----------------------------
@app.post("/predict")
def predict(payload: CarshareInput):

    data = np.array([
        payload.centroid_lat,
        payload.centroid_lon,
        payload.peak_hour
    ]).reshape(1, -1)

    prediction = model.predict(data)[0]

    return {
        "predicted_car_hours": float(prediction)
    }
