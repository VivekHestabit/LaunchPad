import os
import json
import joblib
import numpy as np
import matplotlib.pyplot as plt

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

from src.features.build_features import load_data, engineer_features, build_pipeline
from src.features.feature_selector import correlation_filter, mutual_info_selection, rfe_selection

os.makedirs("./models", exist_ok=True)
os.makedirs("./evaluation", exist_ok=True)

df = load_data()
df = engineer_features(df)

X_train, X_test, y_train, y_test, feature_names = build_pipeline(df)

corr_indices = correlation_filter(X_train, threshold=0.85)
X_train = X_train[:, corr_indices]
X_test = X_test[:, corr_indices]
feature_names = feature_names[corr_indices]

mi_scores = mutual_info_selection(X_train, y_train)

TOP_K = 15
final_indices, final_features = rfe_selection(
    X_train, y_train, feature_names, top_k=TOP_K
)

X_train = X_train[:, final_indices]
X_test = X_test[:, final_indices]

with open("./src/features/feature_list.json", "w") as f:
    json.dump(final_features, f, indent=4)

models = {
    "Logistic Regression (L2)": LogisticRegression(
        penalty="l2",
        C=1.0,
        max_iter=1000
    ),
    "Random Forest": RandomForestClassifier(
        n_estimators=300,
        max_depth=None,
        random_state=42
    ),
    "XGBoost": XGBClassifier(
        eval_metric="logloss",
        learning_rate=0.05,
        max_depth=4,
        n_estimators=300,
        random_state=42
    ),
    "Neural Network": MLPClassifier(
        hidden_layer_sizes=(64, 32),
        alpha=0.001,
        max_iter=500,
        random_state=42
    )
}

cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

results = {}
best_model = None
best_auc = -1

for name, model in models.items():
    print(f"\nTraining {name}...")

    y_pred = cross_val_predict(
        model,
        X_train,
        y_train,
        cv=cv
    )

    y_proba = cross_val_predict(
        model,
        X_train,
        y_train,
        cv=cv,
        method="predict_proba"
    )[:, 1]

    metrics = {
        "accuracy": accuracy_score(y_train, y_pred),
        "precision": precision_score(y_train, y_pred),
        "recall": recall_score(y_train, y_pred),
        "f1": f1_score(y_train, y_pred),
        "roc_auc": roc_auc_score(y_train, y_proba)
    }

    results[name] = metrics

    if metrics["roc_auc"] > best_auc:
        best_auc = metrics["roc_auc"]
        best_model = model

with open("./src/evaluation/metrics.json", "w") as f:
    json.dump(results, f, indent=4)

best_model.fit(X_train, y_train)
joblib.dump(best_model, "./src/models/best_model.pkl")

y_test_pred = best_model.predict(X_test)
cm = confusion_matrix(y_test, y_test_pred)

disp = ConfusionMatrixDisplay(confusion_matrix=cm)
disp.plot()
plt.savefig("./src/evaluation/confusion_matrix.png")
plt.close()

print("\n DAY 3 COMPLETED SUCCESSFULLY")
print(f"Best ROC-AUC: {best_auc:.4f}")
