import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.neural_network import MLPRegressor
from sklearn.svm import SVR
from sklearn.model_selection import cross_val_score
import numpy as np
import time
import os

# Define a dictionary that maps model names to actual model classes
MODEL_CLASSES = {
    'LinearRegression': LinearRegression,
    'DecisionTreeRegressor': DecisionTreeRegressor,
    'GradientBoostingRegressor': GradientBoostingRegressor,
    'RandomForestRegressor': RandomForestRegressor,
    'MLPRegressor': MLPRegressor,
    'SVR': SVR,
    # ……
    # You can continue to add other model classes
    # Beware of importing before use
}

def perform_data_analysis(train_files, validation_files, output_directory, dependent_var, independent_vars, models_config):
    current_time = time.strftime('%Y-%m-%d_%H-%M-%S')
    file_name = os.path.join(output_directory, f"model_evaluation_results_{current_time}.txt")

    with open(file_name, "a") as file:
        file.write(f"Model evaluation results - {time.strftime('%Y-%m-%d %H:%M:%S')}\n")

        # Parsing model configuration
        models = {}
        for model_name, params in models_config.items():
            model_class = MODEL_CLASSES.get(model_name)
            if model_class:
                models[model_name] = model_class(**params)

        for train_file_path, validation_file_path in zip(train_files, validation_files):
            print(f"\nFiles being processed：{os.path.basename(train_file_path)}")
            file.write(f"\nFiles being processed：{os.path.basename(train_file_path)}\n")

            train_data = pd.read_csv(train_file_path)
            validation_data = pd.read_csv(validation_file_path)

            results = {}

            start_time = time.time()

            for model_name, model in models.items():
                print(f"\nStart testing the model：{model_name}")
                for var in independent_vars:
                    print(f"Variable being used：{var}")
                    X_train = train_data[[var]]
                    y_train = train_data[dependent_var]

                    start_cv = time.time()
                    cv_scores = cross_val_score(model, X_train, y_train, cv=5, scoring='r2')
                    end_cv = time.time()

                    cv_duration = end_cv - start_cv

                    key = f"{model_name} with {var}"
                    print(f"Complete：{key}，Time cost：{cv_duration:.2f}sec")

                    results[key] = (cv_scores.mean(), cv_scores, cv_duration)

            end_time = time.time()
            total_duration = end_time - start_time

            best_fit_key = max(results, key=lambda x: results[x][0])
            best_fit_model_name, best_var = best_fit_key.split(" with ")
            best_model = models[best_fit_model_name]

            best_cv_scores = results[best_fit_key][1]
            best_cv_mean_score = results[best_fit_key][0]
            best_cv_duration = results[best_fit_key][2]

            print(f"\nbest fit model：{best_fit_model_name} using variable：{best_var}")
            print(f"cross-validation coefficient of determination：{best_cv_scores}")
            print(f"average coefficient of determination：{best_cv_mean_score}")
            print(f"time required to complete cross-validation：{best_cv_duration:.2f}sec")

            X_train = train_data[[best_var]]
            y_train = train_data[dependent_var]
            best_model.fit(X_train, y_train)

            X_validation = validation_data[[best_var]]
            predictions = best_model.predict(X_validation)

            page_names = validation_data['PageName']

            results_df = pd.DataFrame({
                'PageName': page_names,
                'PredictedFloorSUM': predictions
            })

            results_file = os.path.join(output_directory, f"predictions_{os.path.basename(validation_file_path).replace('.csv', '')}_{current_time}.csv")
            results_df.to_csv(results_file, index=False)

            print(f"\nPredictions have been saved to: {results_file}")
            file.write(f"Best fit model: {best_fit_model_name} using variable: {best_var}, average coefficient of determination: {best_cv_mean_score}\n")
            file.write(f"Predictions have been saved to: {results_file}\n")

    print(f"\nFile write complete")
