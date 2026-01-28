# Week 6 — Day 3: Model Building & Advanced Training

## Objective
The goal of Day-3 was to evaluate whether the prepared dataset (from Day-2) can train reliable machine learning models and to select the best model in a fair and reproducible way.

---

## What We Did

- Built a **unified training pipeline** using `Pipeline` and `ColumnTransformer`
- Applied **proper preprocessing** (scaling, encoding, imputation) inside the pipeline
- Trained **multiple models** on the same data:
  - Logistic Regression
  - Random Forest
  - XGBoost
  - Neural Network (MLP)
- Used **5-fold Stratified Cross-Validation** to avoid overfitting and randomness
- Evaluated models using:
  - Accuracy
  - Precision
  - Recall
  - F1 Score
  - **ROC-AUC (primary metric for churn)**
- Automatically selected and saved the **best model**
- Generated evaluation artifacts:
  - `metrics.json`
  - `confusion_matrix.png`
  - `best_model.pkl`

---

## Key Learnings

- Accuracy alone is misleading for churn problems
- ROC-AUC is more important for class imbalance
- Cross-validation exposes hidden data issues
- Pipelines prevent data leakage and ensure consistency
- Imputation is mandatory for real-world datasets

---

## Final Outcome

- All models were trained successfully
- Neural Network achieved the **best ROC-AUC**
- A production-ready model and evaluation reports were generated

---

## Conclusion

Day-3 validated the data prepared in Day-2 and ensured that model selection was robust, unbiased, and reproducible. This step represents the transition from data preparation to real machine learning engineering.
