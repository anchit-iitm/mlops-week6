import os
import mlflow
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# --- 1. Define Data Schema ---
class IrisFeatures(BaseModel):
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float

# --- 2. Setup FastAPI & Load Model ---
app = FastAPI(title="Iris Classifier API")

# Use the MLFLOW_SERVER_IP from Week 5
# This MUST be the VM's EXTERNAL IP, as GKE is a separate cluster.
MLFLOW_TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI", "http://127.0.0.1:5000")
mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)

model_name = "iris_classifier"
model_stage = "Production"
model_uri = f"models:/{model_name}/{model_stage}"

try:
    print(f"Loading model from: {model_uri}")
    print(f"Connecting to MLflow at: {MLFLOW_TRACKING_URI}")
    model = mlflow.pyfunc.load_model(model_uri)
    print("Model loaded successfully.")
except Exception as e:
    print(f"Error loading model: {e}")
    # If the app can't load the model, it shouldn't start.
    # In a real app, you might handle this more gracefully.
    raise

# --- 3. API Endpoints ---
@app.get("/")
def read_root():
    return {"status": "Iris Classifier API is running."}

@app.post("/predict")
def predict_species(features: IrisFeatures):
    try:
        # Convert Pydantic model to DataFrame for prediction
        # The model expects a DataFrame with these column names
        feature_df = pd.DataFrame([features.dict()])
        
        # Get prediction
        prediction = model.predict(feature_df)
        
        return {
            "predicted_species": prediction[0],
            "input_features": features
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


