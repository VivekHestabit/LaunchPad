import os
import pandas as pd
import logging

RAW_FILE = "src/data/raw/customer_churn_raw.csv"
PROCESSED_FILE = "src/data/processed/final.csv"

os.makedirs("src/logs", exist_ok=True)
os.makedirs("src/data/processed", exist_ok=True)


logging.basicConfig(
    filename='src/logs/data_pipeline.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


def load_data():
    df = pd.read_csv(RAW_FILE)
    logging.info(f"Data loaded from {RAW_FILE} with {len(df)} rows and {len(df.columns)} columns.")
    return df



def clean_data(df):
    num_cols = df.select_dtypes(include='number').columns
    cat_cols = df.select_dtypes(include=['object', 'category']).columns

    df[num_cols] = df[num_cols].fillna(df[num_cols].median())
    for c in cat_cols:
        mode = df[c].mode()
        fill = mode.iloc[0] if not mode.empty else 'missing'
        df[c] = df[c].fillna(fill)

    Q1 = df[num_cols].quantile(0.25)
    Q3 = df[num_cols].quantile(0.75)
    IQR = Q3 - Q1
    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR
    for col in num_cols:
        df[col] = df[col].clip(lower=lower[col], upper=upper[col])

    df = df.drop_duplicates()
    logging.info("Data cleaned: filled missing values, clipped outliers, and removed duplicates.")
    return df


def save_data(df):
    df.to_csv(PROCESSED_FILE, index=False)
    logging.info(f"Cleaned data saved to {PROCESSED_FILE}.")


def main():
    logging.info("Starting the data pipeline.")
    df = load_data()
    logging.info(f"Before cleaning: {len(df)} rows and {len(df.columns)} columns.")
    df = clean_data(df)
    logging.info(f"After cleaning: {len(df)} rows and {len(df.columns)} columns.")
    if df.empty:
        logging.warning("No data left after cleaning. Stopping.")
        print("No data left after cleaning. Stopping.")
        return
    save_data(df)
    logging.info("Data pipeline completed successfully!")
    print("Data pipeline finished successfully!")


if __name__ == "__main__":
    main()