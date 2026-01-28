import os
import numpy as np
import matplotlib.pyplot as plt

from sklearn.feature_selection import mutual_info_classif, RFE
from sklearn.linear_model import LogisticRegression

def correlation_filter(X, threshold=0.85):
    corr = np.corrcoef(X.T)
    drop = set()

    for i in range(len(corr)):
        for j in range(i):
            if abs(corr[i, j]) > threshold:
                drop.add(i)

    keep_indices = [i for i in range(X.shape[1]) if i not in drop]
    return keep_indices

def mutual_info_selection(X, y):
    mi_scores = mutual_info_classif(X, y, random_state=42)
    return mi_scores

def rfe_selection(X, y, feature_names, top_k=15):
    model = LogisticRegression(max_iter=1000)
    rfe = RFE(model, n_features_to_select=top_k)
    rfe.fit(X, y)

    indices = np.where(rfe.support_)[0]
    names = [feature_names[i] for i in indices]

    return indices, names

def plot_feature_importance(mi_scores, feature_names):
    os.makedirs("./src/evaluation", exist_ok=True)

    top_idx = np.argsort(mi_scores)[-20:]

    plt.figure(figsize=(10, 6))
    plt.barh(range(len(top_idx)), mi_scores[top_idx])
    plt.yticks(range(len(top_idx)), [feature_names[i] for i in top_idx])
    plt.title("Top Features by Mutual Information")
    plt.tight_layout()
    plt.savefig("./src/evaluation/feature_importance.png")
    plt.close()

if __name__ == "__main__":
    from build_features import load_data, engineer_features, build_pipeline

    df = load_data()
    df = engineer_features(df)

    X_train, X_test, y_train, y_test, feature_names = build_pipeline(df)

    mi_scores = mutual_info_selection(X_train, y_train)

    plot_feature_importance(mi_scores, feature_names)

    print("Feature importance plot generated at src/evaluation/feature_importance.png")
