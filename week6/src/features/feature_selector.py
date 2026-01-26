import pandas as pd
from sklearn.feature_selection import mutual_info_classif
def correlation_filter(X, threshold=0.9):
    corr = pd.DataFrame(X).corr().abs()
    drop_cols = []

    for i in range(len(corr.columns)):
        for j in range(i):
            if corr.iloc[i, j] > threshold:
                drop_cols.append(corr.columns[i])
                break

    return drop_cols


def mutual_info_selection(X, y, top_k=15):
    mi_scores = mutual_info_classif(X, y, random_state=42)

    mi_df = pd.DataFrame({
        "feature": range(X.shape[1]),
        "score": mi_scores
    }).sort_values(by="score", ascending=False)

    selected_features = mi_df.head(top_k)["feature"].tolist()
    return selected_features, mi_df