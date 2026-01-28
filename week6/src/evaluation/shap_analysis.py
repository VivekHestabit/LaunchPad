import shap
import joblib
import numpy as np
import matplotlib.pyplot as plt

from src.features.build_features import load_data, engineer_features, build_pipeline


MODEL_PATH = "src/models/best_xgboost_model.pkl"
SHAP_SUMMARY_PATH = "src/evaluation/shap_summary.png"
SHAP_IMPORTANCE_PATH = "src/evaluation/shap_feature_importance.png"


def run_shap_analysis():

    # Load and prepare data
    df = load_data()
    df = engineer_features(df)

    X_train, X_test, y_train, y_test, feature_names = build_pipeline(df)

    # Load trained tuned model
    model = joblib.load(MODEL_PATH)

    # SHAP explainer
    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(X_test)

    # -----------------------------
    # 1️⃣ SHAP Summary Plot
    # -----------------------------
    shap.summary_plot(
        shap_values,
        X_test,
        feature_names=feature_names,
        show=False
    )
    plt.savefig(SHAP_SUMMARY_PATH, bbox_inches="tight")
    plt.close()

    # -----------------------------
    # 2️⃣ SHAP-based Feature Importance
    # -----------------------------
    mean_shap = np.abs(shap_values).mean(axis=0)

    top_idx = np.argsort(mean_shap)[::-1][:10]
    top_features = [feature_names[i] for i in top_idx]
    top_values = mean_shap[top_idx]

    plt.figure(figsize=(8, 5))
    plt.barh(top_features[::-1], top_values[::-1])
    plt.xlabel("Mean |SHAP Value|")
    plt.title("Top 10 Features by SHAP Importance")
    plt.tight_layout()
    plt.savefig(SHAP_IMPORTANCE_PATH, bbox_inches="tight")
    plt.close()

    print("SHAP analysis completed.")
    print(f"Saved: {SHAP_SUMMARY_PATH}")
    print(f"Saved: {SHAP_IMPORTANCE_PATH}")


if __name__ == "__main__":
    run_shap_analysis()
