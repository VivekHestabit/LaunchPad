import shap
import joblib
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

from sklearn.model_selection import train_test_split

from src.features.build_features import load_data, engineer_features, build_pipeline

MODEL_PATH = "src/models/best_xgboost_model.pkl"
PREPROCESSOR_PATH = "src/models/preprocessor_v1.pkl"

SHAP_SUMMARY_PATH = "src/evaluation/shap_summary.png"
SHAP_IMPORTANCE_PATH = "src/evaluation/shap_feature_importance.png"


def get_feature_names(preprocessor):
    num_features = preprocessor.transformers_[0][2]
    cat_encoder = preprocessor.transformers_[1][1]
    cat_features = preprocessor.transformers_[1][2]

    cat_feature_names = cat_encoder.get_feature_names_out(cat_features)

    return np.concatenate([num_features, cat_feature_names])


def run_shap_analysis():

    df = load_data()
    df = engineer_features(df)

    X, y, preprocessor = build_pipeline(df)

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y
    )

    preprocessor = joblib.load(PREPROCESSOR_PATH)
    model = joblib.load(MODEL_PATH)

    X_test_transformed = preprocessor.transform(X_test)

    if hasattr(X_test_transformed, "toarray"):
        X_test_transformed = X_test_transformed.toarray()

    feature_names = get_feature_names(preprocessor)

    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(X_test_transformed)

    shap.summary_plot(
        shap_values,
        X_test_transformed,
        feature_names=feature_names,
        show=False
    )

    plt.savefig(SHAP_SUMMARY_PATH, bbox_inches="tight")
    plt.close()

    mean_shap = np.abs(shap_values).mean(axis=0)
    top_idx = np.argsort(mean_shap)[::-1][:10]

    top_features = feature_names[top_idx]
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
