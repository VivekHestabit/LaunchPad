import os
import pandas as pd
import numpy as np
from scipy import stats
from src.utils.logger import logger

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

RAW_DATA_PATH = os.path.join(BASE_DIR, "data", "raw", "Titanic-Dataset.csv")
PROCESSED_DATA_PATH = os.path.join(BASE_DIR, "data", "processed", "final.csv")

os.makedirs(os.path.dirname(PROCESSED_DATA_PATH), exist_ok=True)

def load_data():
    df = pd.read_csv(RAW_DATA_PATH)
    print(f"Loaded data shape: {df.shape}")
    logger.info(
        f"LOAD | Raw data loaded | Rows: {df.shape[0]} | Columns: {df.shape[1]}"
    )
    return df

def clean_data(df):
    before_rows = df.shape[0]

    df = df.drop_duplicates()

    DROP_COLS = ["PassengerId", "Ticket", "Cabin", "Name"]
    df = df.drop(columns=DROP_COLS, errors="ignore")

    df["Age"] = df["Age"].fillna(df["Age"].median())
    df["Fare"] = df["Fare"].fillna(df["Fare"].median())
    df["Embarked"] = df["Embarked"].fillna(df["Embarked"].mode()[0])

    df["Sex"] = df["Sex"].map({"male": 0, "female": 1})
    
    after_rows = df.shape[0]

    logger.info(
        f"CLEAN | Rows before: {before_rows} | Rows after: {after_rows}"
    )
    return df

def handle_outliers(df):
    before_rows = df.shape[0]
    numeric_cols = ["Age", "Fare"]

    for col in numeric_cols:
        z_scores = np.abs(stats.zscore(df[col]))
        df = df[z_scores < 3]
        
    after_rows = df.shape[0]

    logger.info(
        f"OUTLIERS | Rows before: {before_rows} | Rows after: {after_rows}"
    )

    return df

def save_data(df):
    df.to_csv(PROCESSED_DATA_PATH, index=False)
    logger.info(
        f"SAVE | Cleaned data saved | Final rows: {df.shape[0]} | Path: {PROCESSED_DATA_PATH}"
    )
    print(f"Cleaned data saved to: {PROCESSED_DATA_PATH}")

def run_pipeline():
    logger.info("PIPELINE STARTED")
    df = load_data()
    df = clean_data(df)
    df = handle_outliers(df)
    save_data(df)
    
    logger.info("PIPELINE COMPLETED SUCCESSFULLY")

if __name__ == "__main__":
    run_pipeline()
