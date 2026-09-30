import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, root_mean_squared_error, mean_absolute_error
import bentoml

PROCESSED_DATA_PATH = "data/processed"
MODEL_NAME ="admission_lr"

def load_processed_data(input_dir):
    X_train = pd.read_csv(f"{input_dir}/X_train.csv")
    X_test = pd.read_csv(f"{input_dir}/X_test.csv")
    y_train = pd.read_csv(f"{input_dir}/y_train.csv")
    y_test = pd.read_csv(f"{input_dir}/y_test.csv")
    y_train = np.ravel(y_train)
    y_test = np.ravel(y_test)
    return X_train, X_test, y_train, y_test

def train_model(X_train, y_train):
    model = LinearRegression()
    model.fit(X_train, y_train)
    return model

def evaluate_model(model, X_test, y_test):
    y_pred = model.predict(X_test)
    r2 = r2_score(y_test, y_pred)
    return r2

if __name__ == "__main__":
    X_train, X_test, y_train, y_test = load_processed_data(PROCESSED_DATA_PATH)
    model = train_model(X_train, y_train)
    metric = evaluate_model(model, X_test, y_test)

    print(f"R2: {metric}")

    model_ref = bentoml.sklearn.save_model(MODEL_NAME, model)
    print(f"Model saved as: {model_ref}")