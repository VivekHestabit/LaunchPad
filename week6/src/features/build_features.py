import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer

DATA_PATH = "./src/data/processed/final.csv"

def load_data():
    return pd.read_csv(DATA_PATH)

def engineer_features(df):
    df["FamilySize"] = df["SibSp"] + df["Parch"] + 1
    df["IsAlone"] = (df["FamilySize"] == 1).astype(int)

    df["FarePerPerson"] = df["Fare"] / df["FamilySize"]
    df["LogFare"] = np.log1p(df["Fare"])
    df["SqrtFare"] = np.sqrt(df["Fare"])

    df["AgeGroup"] = pd.cut(
        df["Age"],
        bins=[0, 12, 18, 35, 60, 100],
        labels=["Child", "Teen", "YoungAdult", "Adult", "Senior"]
    )

    df["ChildFlag"] = (df["Age"] < 12).astype(int)
    df["ElderFlag"] = (df["Age"] > 60).astype(int)

    df["ClassFareInteraction"] = df["Pclass"] * df["Fare"]

    return df

def build_pipeline(df):
    y = df["Survived"]
    X = df.drop(columns=["Survived"])

    categorical = ["Sex", "Embarked", "AgeGroup"]
    numerical = [c for c in X.columns if c not in categorical]

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), numerical),
            ("cat", OneHotEncoder(drop="first", handle_unknown="ignore"), categorical)
        ]
    )

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        stratify=y,
        random_state=42
    )

    X_train = preprocessor.fit_transform(X_train)
    X_test = preprocessor.transform(X_test)

    feature_names = preprocessor.get_feature_names_out()

    return X_train, X_test, y_train, y_test, feature_names

if __name__ == "__main__":
    df = load_data()
    df = engineer_features(df)

    X_train, X_test, y_train, y_test, feature_names = build_pipeline(df)

    print(" Day 2 feature engineering completed successfully")
