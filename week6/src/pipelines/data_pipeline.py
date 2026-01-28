import os
import pandas as pd
import numpy as np
from scipy import stats

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

RAW_DATA_PATH = os.path.join(BASE_DIR, "data", "raw", "Titanic-Dataset.csv")
PROCESSED_DATA_PATH = os.path.join(BASE_DIR, "data", "processed", "final.csv")

os.makedirs(os.path.dirname(PROCESSED_DATA_PATH), exist_ok=True)

def load_data():
    df = pd.read_csv(RAW_DATA_PATH)
    print(f"Loaded data shape: {df.shape}")
    return df

def clean_data(df):
    df = df.drop_duplicates()

    DROP_COLS = ["PassengerId", "Ticket", "Cabin", "Name"]
    df = df.drop(columns=DROP_COLS, errors="ignore")

    df["Age"] = df["Age"].fillna(df["Age"].median())
    df["Fare"] = df["Fare"].fillna(df["Fare"].median())
    df["Embarked"] = df["Embarked"].fillna(df["Embarked"].mode()[0])

    df["Sex"] = df["Sex"].map({"male": 0, "female": 1})

    return df

def handle_outliers(df):
    numeric_cols = ["Age", "Fare"]

    for col in numeric_cols:
        z_scores = np.abs(stats.zscore(df[col]))
        df = df[z_scores < 3]

    return df

def save_data(df):
    df.to_csv(PROCESSED_DATA_PATH, index=False)
    print(f"Cleaned data saved to: {PROCESSED_DATA_PATH}")

def run_pipeline():
    df = load_data()
    df = clean_data(df)
    df = handle_outliers(df)
    save_data(df)

if __name__ == "__main__":
    run_pipeline()
