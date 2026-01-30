from fastapi import FastAPI, HTTPException
from pydantic import BaseModel , Field , validator
from datetime import datetime, timezone
import uuid
import joblib
import pandas as pd
import os
import csv
from typing import Literal

MODEL_PATH = "src/models/model_v1.pkl"
LOG_PATH = "src/logs/prediction_logs.csv"

app = FastAPI(title="Titanic Survival Prediction API")

try:
    pipeline = joblib.load(MODEL_PATH)
except Exception as e:
    raise RuntimeError(f"Failed to load model pipeline: {e}")

@app.get("/health")
def health():
    return {"status": "UP", "timestamp": datetime.now(timezone.utc).isoformat()}

class PredictionRequest(BaseModel):
    
    Age: float = Field(... , ge=0 , description="Passenger age (>=0)")
    Sex: Literal["male" , "Female"]
    Pclass: Literal[1,2,3]
    Fare: float = Field(... , ge=0 , description="Ticket Fare (>=0)")
    SibSp: int = Field(... , ge=0)
    Parch: int = Field(... , ge=0)
    Embarked: Literal["C" , "Q" , "S"]

def log_prediction(data: dict):
    
    os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
    file_exists = os.path.isfile(LOG_PATH)
    with open(LOG_PATH, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=data.keys())
        if not file_exists:
            writer.writeheader()
        writer.writerow(data)

@app.post("/predict")
def predict(request: PredictionRequest):
    
    request_id = str(uuid.uuid4())
    timestamp = datetime.now(timezone.utc).isoformat()
    try:
        df = pd.DataFrame([request.dict()])
        prediction = int(pipeline.predict(df)[0])
        probability = None
        if hasattr(pipeline.named_steps["model"], "predict_proba"):
            probability = float(pipeline.predict_proba(df)[0][1])
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    log_data = {"timestamp": timestamp, "request_id": request_id, **request.dict(), "prediction": prediction, "probability": probability}
    log_prediction(log_data)
    
    return {"request_id": request_id, "prediction": prediction, "probability": probability}
