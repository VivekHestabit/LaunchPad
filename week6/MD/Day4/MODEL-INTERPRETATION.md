Day 4 Model Tuning and Explainability

1. What was done

2. XGBoost was selected as the best performing model from Day 3

3. Hyperparameters were tuned using Optuna to improve model performance

4. The tuned model was trained using the training dataset

5. The final model was evaluated on the test dataset

6. SHAP was used to explain model predictions

7. Why it was done

8. To check whether default XGBoost parameters were optimal

9. To improve model performance in a controlled manner

10. To understand how the model makes decisions

11. To detect overfitting and variance issues early

12. Results

13. Cross validation ROC AUC improved after hyperparameter tuning

14. Test ROC AUC and recall decreased slightly

15. This behavior was expected due to the small size of the Titanic dataset

16. The tuned model showed signs of increased variance and mild overfitting

17. Explainability insights

18. Gender was the most influential feature for survival prediction

19. Younger passengers had a higher probability of survival

20. Passenger class and fare strongly influenced predictions

21. The model learned patterns consistent with real Titanic rescue behavior

22. Key learnings

23. Hyperparameter tuning improves training performance but does not guarantee better test performance

24. Powerful models can overfit on small datasets

25. Explainability is essential to trust and validate model behavior

26. Understanding model limitations is as important as improving metrics