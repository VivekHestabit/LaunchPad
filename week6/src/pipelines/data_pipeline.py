import os
import pandas as pd

RAW_FILE = "src/data/raw/online_retail_customer_churn.csv"
PROCESSED_FILE = "src/data/processed/final.csv"

os.makedirs("src/data/processed", exist_ok=True)

def load_data():
    df = pd.read_csv(RAW_FILE)
    print(f"Loaded data with {len(df)} rows and {len(df.columns)} columns.")
    return df

def clean_data(df):
    df = df.dropna()
    print(f"After removing missing values: {len(df)} rows.")
    df = df.drop_duplicates()
    print(f"After removing duplicates: {len(df)} rows.")
    return df

def save_data(df):
    df.to_csv(PROCESSED_FILE, index=False)
    print("Saved cleaned data to processed folder.")

def main():
    print("Starting data pipeline...")
    df = load_data()
    df = clean_data(df)
    if df.empty:
        print("No data left after cleaning. Stopping.")
        return
    save_data(df)
    print("Data pipeline finished successfully!")

if __name__ == "__main__":
    main()
