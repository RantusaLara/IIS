import pandas as pd

from sklearn.linear_model import LinearRegression

import pickle as pkl
from joblib import dump, load
from sklearn.metrics import mean_absolute_error, mean_squared_error, explained_variance_score


import mlflow 

MLFLOW_TRACKING_URI = "https://dagshub.com/RantusaLara/IIS.mlflow" 
mlflow.set_tracking_url(MLFLOW_TRACKING_URI)
mlflow.set_experiment("my_experiment") 
mlflow.autolog(exclusive=False)

with mlflow.start_run():
    df = pd.read_csv("data/processed/current_data.csv", sep = ",", decimal = ".")
    n = int(len(df) * 0.1)
    test_df = df.head(n)
    train_df = df.tail(len(df) - n)

    X_train = train_df.drop('pm10', axis=1)
    X_train = train_df.drop('date', axis=1)
    y_train = train_df['pm10']

    model = LinearRegression()
    model.fit(X_train, y_train)

    result = model.predict(X_train)

    mae = mean_absolute_error(y_train, result)
    mse = mean_squared_error(y_train, result)
    evs = explained_variance_score(y_train, result)

    mlflow.log_metric("MAE", mae)
    mlflow.log_metric("MSE", mse)
    mlflow.log_metric("EVS", evs)

autolog_run = mlflow.last_active_run()