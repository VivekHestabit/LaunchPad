import optuna
import json
import joblib
import xgboost as xgb
import numpy as np

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score
)
from sklearn.model_selection import StratifiedKFold

from src.features.build_features import load_data, engineer_features, build_pipeline

RESULTS_PATH = "src/tuning/results.json"
MODEL_PATH = "src/models/best_xgboost_model.pkl"

def objective(trial, X, y, scale_pos_weight):
    params = {
        "n_estimators": trial.suggest_int("n_estimators", 100, 500),
        "max_depth": trial.suggest_int("max_depth", 3, 8),
        "learning_rate": trial.suggest_float("learning_rate", 0.01, 0.3),
        "subsample": trial.suggest_float("subsample", 0.6, 1.0),
        "colsample_bytree": trial.suggest_float("colsample_bytree", 0.6, 1.0),
        "gamma": trial.suggest_float("gamma", 0, 5),
        "min_child_weight": trial.suggest_int("min_child_weight", 1, 10),
        "scale_pos_weight": scale_pos_weight,
        "eval_metric": "auc",
        "use_label_encoder": False,
        "random_state": 42,
        "n_jobs": -1
    }
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    auc_scores = []
    for train_idx, val_idx in cv.split(X, y):
        X_tr, X_val = X[train_idx, :], X[val_idx, :]
        y_tr, y_val = y.iloc[train_idx], y.iloc[val_idx]
        model = xgb.XGBClassifier(**params)
        model.fit(X_tr, y_tr)
        probs = model.predict_proba(X_val)[:, 1]
        auc_scores.append(roc_auc_score(y_val, probs))
    return np.mean(auc_scores)

def tune_and_train(X_train, X_test, y_train, y_test):
    scale_pos_weight = (y_train == 0).sum() / (y_train == 1).sum()
    study = optuna.create_study(direction="maximize")
    study.optimize(
        lambda trial: objective(trial, X_train, y_train, scale_pos_weight),
        n_trials=50
    )
    best_params = study.best_params
    with open(RESULTS_PATH, "w") as f:
        json.dump(best_params, f, indent=4)
    print("Best hyperparameters saved")
    print("Best CV ROC-AUC:", study.best_value)
    final_model = xgb.XGBClassifier(
        **best_params,
        scale_pos_weight=scale_pos_weight,
        eval_metric="auc",
        use_label_encoder=False,
        random_state=42,
        n_jobs=-1
    )
    final_model.fit(X_train, y_train)
    preds = final_model.predict(X_test) 
    probs = final_model.predict_proba(X_test)[:, 1]
    metrics = {
        "accuracy": accuracy_score(y_test, preds),
        "precision": precision_score(y_test, preds),
        "recall": recall_score(y_test, preds),
        "f1": f1_score(y_test, preds),
        "roc_auc": roc_auc_score(y_test, probs)
    }
    print("\nFinal Tuned XGBoost Metrics:")
    for k, v in metrics.items():
        print(f"{k}: {v:.4f}")
    joblib.dump(final_model, MODEL_PATH)
    print(f"\nFinal model saved at {MODEL_PATH}")

if __name__ == "__main__":
    df = load_data()
    df = engineer_features(df)
    X_train, X_test, y_train, y_test, feature_names = build_pipeline(df)
    tune_and_train(X_train, X_test, y_train, y_test)