import os
import json
import joblib
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import FunctionTransformer
from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, confusion_matrix, ConfusionMatrixDisplay
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
from xgboost import XGBClassifier
from src.features.build_features import load_data, engineer_features, build_pipeline

MODEL_DIR = "src/models"
EVAL_DIR = "src/evaluation"
os.makedirs(MODEL_DIR, exist_ok=True)
os.makedirs(EVAL_DIR, exist_ok=True)

df = load_data()
df = engineer_features(df)
X, y, preprocessor = build_pipeline(df)

models = {
    "Logistic Regression": LogisticRegression(penalty="l2", C=1.0, max_iter=1000),
    "Random Forest": RandomForestClassifier(n_estimators=300, random_state=42),
    "XGBoost": XGBClassifier(eval_metric="logloss", learning_rate=0.05, max_depth=4, n_estimators=300, random_state=42),
    "Neural Network": MLPClassifier(hidden_layer_sizes=(64, 32), alpha=0.001, max_iter=500, random_state=42)
}

cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
results = {}
best_model = None
best_auc = -1

for name, model in models.items():
    print(f"\nEvaluating {name}...")
    pipeline = Pipeline([("preprocessor", preprocessor), ("model", model)])
    auc_scores = cross_val_score(pipeline, X, y, cv=cv, scoring="roc_auc")
    results[name] = {"roc_auc_mean": float(np.mean(auc_scores)), "roc_auc_std": float(np.std(auc_scores))}
    if np.mean(auc_scores) > best_auc:
        best_auc = np.mean(auc_scores)
        best_model = model

with open(f"{EVAL_DIR}/metrics.json", "w") as f:
    json.dump(results, f, indent=4)

print(f"\nBest model selected with ROC-AUC: {best_auc:.4f}")

feature_engineering = FunctionTransformer(engineer_features, validate=False)

final_pipeline = Pipeline([("feature_engineering", feature_engineering), ("preprocessor", preprocessor), ("model", best_model)])

final_pipeline.fit(X, y)
joblib.dump(final_pipeline, "src/models/model_v1.pkl")
print(" model_v1.pkl saved successfully")

y_pred = final_pipeline.predict(X)
cm = confusion_matrix(y, y_pred)
disp = ConfusionMatrixDisplay(confusion_matrix=cm)
disp.plot()
plt.savefig(f"{EVAL_DIR}/confusion_matrix.png")
plt.close()
print(" Training complete and deployment-ready")
