# Carshare Prediction System

This project predicts carshare usage hours using an XGBoost regression model.

## Features

- FastAPI backend
- Streamlit frontend
- XGBoost ML model
- Real-time prediction API

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Run FastAPI

```bash
uvicorn app:app --reload
```

---

## Run Streamlit

```bash
streamlit run streamit_app.py
```

---

## API Endpoint

POST `/predict`

Example Request:

```json
{
  "centroid_lat": 44.98,
  "centroid_lon": -93.26,
  "peak_hour": 17
}
```