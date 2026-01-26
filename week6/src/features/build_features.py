import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer

DATA_PATH = "src/data/processed/final.csv"

def load_data():
    df = pd.read_csv(DATA_PATH)
    df = convert_to_numeric(df)
    return df


def convert_to_numeric(df):
    numeric_cols = [
        "Total_Spend",
        "Annual_Income",
        "Years_as_Customer",
        "Num_of_Purchases",
        "Num_of_Returns",
        "Num_of_Support_Contacts",
        "Satisfaction_Score",
        "Last_Purchase_Days_Ago"
    ]

    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")
        
        binary_cols = ["Promotion_Response", "Email_Opt_In"]

    for col in binary_cols:
        df[col] = df[col].map({"Yes": 1, "No": 0})

    return df


def create_features(df):
    df["spend_per_year"] = df["Total_Spend"] / df["Years_as_Customer"]
    df["spend_per_purchase"] = df["Total_Spend"] / df["Num_of_Purchases"]
    df["income_spend_ratio"] = df["Total_Spend"] / df["Annual_Income"]

    df["purchase_frequency"] = df["Num_of_Purchases"] / df["Years_as_Customer"]
    df["return_rate"] = df["Num_of_Returns"] / df["Num_of_Purchases"]
    df["support_contact_rate"] = df["Num_of_Support_Contacts"] / df["Years_as_Customer"]

    df["inactive_flag"] = (df["Last_Purchase_Days_Ago"] > 90).astype(int)
    df["low_satisfaction_flag"] = (df["Satisfaction_Score"] < 3).astype(int)
    df["high_support_flag"] = (df["Num_of_Support_Contacts"] > 3).astype(int)

    df["promo_effective"] = df["Promotion_Response"] * df["Email_Opt_In"]
    df["loyalty_score"] = df["Years_as_Customer"] * df["Satisfaction_Score"]

    return df

def build_pipeline(df):
    y = df["Target_Churn"]
    X = df.drop(columns=["Target_Churn", "Customer_ID"])

    categorical = ["Gender"]
    numerical = [col for col in X.columns if col not in categorical]

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), numerical),
            ("cat", OneHotEncoder(drop="first"), categorical)
        ]
    )

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    X_train = preprocessor.fit_transform(X_train) 
    X_test = preprocessor.transform(X_test)

    return X_train, X_test, y_train, y_test, preprocessor

if __name__ == "__main__":
    df = load_data()
    df = create_features(df)
    X_train, X_test, y_train, y_test, pipeline = build_pipeline(df)