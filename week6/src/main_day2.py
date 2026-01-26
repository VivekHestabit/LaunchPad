import pandas as pd
import matplotlib.pyplot as plt

from features.build_features import load_data, create_features, build_pipeline
from features.feature_selector import correlation_filter, mutual_info_selection

df = load_data()
print(df.dtypes)
df = create_features(df)

X_train, X_test, y_train, y_test , preprocessor = build_pipeline(df)

X_train_df = pd.DataFrame(X_train)
X_test_df = pd.DataFrame(X_test)


X_train_df = X_train_df.fillna(0)
X_test_df = X_test_df.fillna(0)

drop_cols = correlation_filter(X_train_df)
X_train_df = X_train_df.drop(columns=drop_cols)
X_test_df = X_test_df.drop(columns=drop_cols)

selected_idx, mi_df = mutual_info_selection(X_train_df, y_train)


X_train_final = X_train_df.iloc[:, selected_idx]
X_test_final = X_test_df.iloc[:, selected_idx]

plt.figure(figsize=(8,5))
plt.barh(mi_df.head(15)["feature"], mi_df.head(15)["score"])
plt.xlabel("Mutual Information Score")
plt.ylabel("Feature Index")
plt.title("Top Features for Churn Prediction")
plt.tight_layout()
plt.savefig('src/features/feature_importance.png')
plt.close()
