# Titanic — Feature Engineering (Day 2)

## Objective
Create meaningful, interpretable features to improve survival prediction.

## Engineered Features
- FamilySize: total family members aboard
- IsAlone: passenger traveling alone
- FarePerPerson: normalized fare by family size
- HighFareFlag: indicator of high socio-economic status
- AgeGroup: categorical age buckets
- ChildFlag / ElderFlag: vulnerability indicators
- SibSp_gt_0 / Parch_gt_0: relationship presence
- ClassFareInteraction: socio-economic interaction

## Encoding Strategy
- OneHotEncoding: Embarked, AgeGroup
- Numerical Scaling: StandardScaler

## Feature Selection
- Mutual Information used to rank features by predictive power

## Output
- Feature pipeline ready
- X_train, X_test, y_train, y_test prepared
- Feature list saved for reproducibility
