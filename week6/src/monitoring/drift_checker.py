import pandas as pd
import numpy as np
import json
import os

TRAIN_DATA_PATH = "src/data/processed/final.csv"
PREDICTION_LOG_PATH = "src/logs/prediction_logs.csv"
OUTPUT_PATH = "src/monitoring/drift_report.json"

NUMERIC_FEATURES = [
    "Age",
    "Fare",
    "Sibsp",
    "Parch"
]

def calculate_psi(expected, actual, bins=10):
    expected = np.array(expected)
    actual = np.array(actual)

    breakpoints = np.percentile(expected, np.linspace(0, 100, bins + 1))
    breakpoints = np.unique(breakpoints)

    expected_counts = np.histogram(expected, bins=breakpoints)[0]
    actual_counts = np.histogram(actual, bins=breakpoints)[0]

    expected_perc = expected_counts / len(expected)
    actual_perc = actual_counts / len(actual)

    psi = 0.0
    for e, a in zip(expected_perc, actual_perc):
        if e == 0 or a == 0:
            continue
        psi += (a - e) * np.log(a / e)

    return round(float(psi), 4)

def run_drift_check():
    if not os.path.exists(PREDICTION_LOG_PATH):
        print(" Prediction logs not found ")
        return

    train_df = pd.read_csv(TRAIN_DATA_PATH)
    pred_df = pd.read_csv(PREDICTION_LOG_PATH)

    if pred_df.empty or len(pred_df) < 5:
        print(" Not enough prediction data to compute drift ")
        return

    pred_df.columns = pred_df.columns.str.capitalize()
    train_df.columns = train_df.columns.str.capitalize()

    drift_results = {}

    for feature in NUMERIC_FEATURES:
        if feature not in pred_df.columns or feature not in train_df.columns:
            continue

        psi_value = calculate_psi(
            train_df[feature].dropna(),
            pred_df[feature].dropna()
        )

        if psi_value < 0.1:
            status = "NO_DRIFT"
        elif psi_value < 0.25:
            status = "MODERATE_DRIFT"
        else:
            status = "SEVERE_DRIFT"

        drift_results[feature] = {
            "psi": psi_value,
            "status": status
        }

    if not drift_results:
        print(" No drift calculated — check feature names or data ")
        return

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

    with open(OUTPUT_PATH, "w") as f:
        json.dump(drift_results, f, indent=4)

    print("✅ Drift check completed successfully")
    print(json.dumps(drift_results, indent=4))

if __name__ == "__main__":
    run_drift_check()
