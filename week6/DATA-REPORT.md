DAY 1 — Data Pipeline & EDA
Project

Online Transaction Customer Churn Prediction

Objective

Build a reproducible data pipeline to clean raw data and perform initial exploratory data analysis (EDA).

Dataset

Source: Online Transaction Customer Churn dataset

Type: Tabular (numerical + categorical)

Target: Customer Churn

Data Pipeline

Loaded raw data from data/raw/

Removed duplicate records

Handled missing values:

Numerical features: median imputation

Categorical features: mode imputation

Handled outliers using IQR-based clipping

Saved cleaned dataset to data/processed/final.csv

Exploratory Data Analysis

Feature distributions analyzed

Target class distribution analyzed

Correlation matrix generated for numerical features

Missing values heatmap visualized

Deliverables

pipelines/data_pipeline.py

notebooks/EDA.ipynb

data/processed/final.csv

DATA-REPORT.md

Outcome

A clean, analysis-ready dataset and baseline EDA insights were generated to support further feature engineering and model development.