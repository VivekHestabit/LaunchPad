# Day 1 — Data Pipeline & EDA Report (Titanic)

## Dataset Overview
- Rows: 891
- Target: Survived (Binary)
- Problem Type: Binary Classification

## Data Cleaning
- Removed duplicate records
- Filled missing Age values using median
- Filled missing Embarked using mode
- Dropped Cabin, Ticket, PassengerId, Name due to high missing or irrelevance

## Outlier Handling
- Fare outliers capped using IQR method

## EDA Insights
- Survival rate is imbalanced (~38% survived)
- Females had significantly higher survival rates
- First-class passengers survived more
- Fare is positively correlated with survival
- Age shows non-linear relationship with survival

## Conclusion
The dataset is clean, consistent, and suitable for feature engineering and model training.

## Status
✔ Day 1 completed  
✔ Ready for Day 2
