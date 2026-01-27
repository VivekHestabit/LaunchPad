import json
import joblib
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.impute import SimpleImputer

from sklearn.model_selection import StratifiedKFold, cross_val_predict
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
    ConfusionMatrixDisplay
)

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
from xgboost import XGBClassifier

from sklearn.preprocessing import StandardScaler, OneHotEncoder, LabelEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

DATA_PATH = "../data/processed/final.csv"
df = pd.read_csv(DATA_PATH)

df["Annual_Income"] = (
    df["Annual_Income"]
    .astype(str)
    .str.replace("$", "", regex=False)
    .str.replace(",", "", regex=False)
)

df["Annual_Income"] = pd.to_numeric(df["Annual_Income"], errors="coerce")

le = LabelEncoder()
df["Target_Churn"] = le.fit_transform(df["Target_Churn"])

y = df["Target_Churn"]
X = df.drop(columns=["Target_Churn", "Customer_ID"])

categorical_cols = ["Gender", "Email_Opt_In", "Promotion_Response"]
numerical_cols = [col for col in X.columns if col not in categorical_cols]

preprocessor = ColumnTransformer(
    transformers=[
        (
            "num",
            Pipeline([
                ("imputer", SimpleImputer(strategy="median")),
                ("scaler", StandardScaler())
            ]),
            numerical_cols
        ),
        (
            "cat",
            Pipeline([
                ("imputer", SimpleImputer(strategy="most_frequent")),
                ("encoder", OneHotEncoder(drop="first", handle_unknown="ignore"))
            ]),
            categorical_cols
        )
    ]
)

models = {
    "Logistic Regression": Pipeline([
        ("preprocessor", preprocessor),
        ("model", LogisticRegression(max_iter=1000))
    ]),

    "Random Forest": Pipeline([
        ("preprocessor", preprocessor),
        ("model", RandomForestClassifier(n_estimators=200, random_state=42))
    ]),

    "XGBoost": Pipeline([
        ("preprocessor", preprocessor),
        ("model", XGBClassifier(eval_metric="logloss", random_state=42))
    ]),

    "Neural Network": Pipeline([
        ("preprocessor", preprocessor),
        ("model", MLPClassifier(hidden_layer_sizes=(64, 32), max_iter=500, random_state=42))
    ])
}

skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

results = {}
best_model = None
best_auc = -1

for name, model in models.items():
    print(f"Training {name}...")

    y_pred = cross_val_predict(model, X, y, cv=skf)
    y_proba = cross_val_predict(
        model, X, y, cv=skf, method="predict_proba"
    )[:, 1]

    metrics = {
        "accuracy": accuracy_score(y, y_pred),
        "precision": precision_score(y, y_pred),
        "recall": recall_score(y, y_pred),
        "f1": f1_score(y, y_pred),
        "roc_auc": roc_auc_score(y, y_proba)
    }

    results[name] = metrics

    if metrics["roc_auc"] > best_auc:
        best_auc = metrics["roc_auc"]
        best_model = model

best_model.fit(X, y)

joblib.dump(best_model, "../models/best_model.pkl")

with open("../evaluation/metrics.json", "w") as f:
    json.dump(results, f, indent=4)

y_final_pred = best_model.predict(X)
cm = confusion_matrix(y, y_final_pred)

disp = ConfusionMatrixDisplay(confusion_matrix=cm)
disp.plot()
plt.savefig("../evaluation/confusion_matrix.png")
plt.close()

print("\n Day-3 Training Completed Successfully")
