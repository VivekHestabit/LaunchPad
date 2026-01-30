# Deployment Notes – Day 5 (ML Model Deployment & Monitoring)

## Overview
This project deploys a trained Titanic survival prediction model as a REST API using FastAPI.  
The goal was to build a production-ready ML pipeline with proper preprocessing, logging, monitoring, and Docker support.

---

## Training Flow
- Raw data is loaded and feature engineering is applied.
- Preprocessing (scaling + encoding) is defined using `ColumnTransformer`.
- Feature engineering, preprocessing, and the model are combined into a **single sklearn Pipeline**.
- This pipeline is trained and saved as `model_v1.pkl`.

Using a single pipeline avoids training–serving skew.

---

## API Design
- FastAPI is used for model serving.
- `/health` endpoint checks service status.
- `/predict` endpoint accepts passenger details and returns:
  - prediction (0 = not survived, 1 = survived)
  - probability
  - request_id for traceability
- Input validation is enforced using Pydantic.

---

## Logging
- Each prediction request is logged to `prediction_logs.csv`.
- Logs include timestamp, request_id, input features, prediction, and probability.
- Logs are persisted using Docker volume mounts.

---

## Monitoring (Data Drift)
- A drift checker script compares training data with live prediction data.
- Population Stability Index (PSI) is used for numeric features.
- Drift results are saved to `drift_report.json`.
- PSI thresholds:
  - < 0.1 → No drift
  - 0.1–0.25 → Moderate drift
  - > 0.25 → Severe drift

---

## Running the Project

### Train Model
python src/training/train.py
