import plotly.express as px
import pandas as pd
from sklearn.model_selection import train_test_split
from xgboost import XGBRegressor
import pickle

# ------------------------------------------------
# Load dataset from Plotly
# ------------------------------------------------
carshare = px.data.carshare()

print("Columns:", carshare.columns.tolist())

# carshare columns:
# ['centroid_lat', 'centroid_lon', 'car_hours', 'peak_hour']

# ------------------------------------------------
# Features & Target
# ------------------------------------------------
X = carshare[['centroid_lat', 'centroid_lon', 'peak_hour']]
y = carshare['car_hours']

# ------------------------------------------------
# Train–test split
# ------------------------------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# ------------------------------------------------
# Train XGBoost (no scaling required)
# ------------------------------------------------
model = XGBRegressor(
    n_estimators=300,
    learning_rate=0.05,
    max_depth=4,
    subsample=0.9,
    colsample_bytree=0.9,
    objective='reg:squarederror',
    random_state=42
)

model.fit(X_train, y_train)

# ------------------------------------------------
# Save pickle file
# ------------------------------------------------
with open("xgb_carshare_model.pkl", "wb") as f:
    pickle.dump(model, f)

print("Model trained successfully and saved as xgb_carshare_model.pkl")
