FEATURE ENGINEERING — DAY 2
Objective

Transform cleaned customer data into meaningful, model-ready features and select the most useful ones for churn prediction.

Feature Engineering

Created new features to capture customer behavior and engagement, including:

Spend efficiency (e.g. spend per year, spend per purchase)

Customer activity (purchase frequency, inactivity flag)

Support and dissatisfaction signals (return rate, support contact rate)

Interaction and loyalty signals (promo effectiveness, loyalty score)

Total engineered features: 11

Data Preparation

Converted string-based numeric columns to proper numeric format

Encoded categorical features using One-Hot Encoding

Scaled numerical features using StandardScaler

Split data into training and testing sets with stratification

Feature Selection

Applied feature selection to reduce noise and redundancy:

Correlation-based filtering to remove highly correlated features

Mutual Information to measure feature relevance to churn

Top features were selected based on importance scores.

Outputs

ML-ready datasets: X_train, X_test, y_train, y_test

Feature importance plot saved as an artifact

Feature metadata stored for reproducibility

Outcome

A clean, validated feature set prepared for model training in Day 3.