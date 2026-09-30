import pandas as pd
from sklearn.model_selection import train_test_split
from pathlib import Path

RAW_DATA_PATH = "data/raw/admission.csv"
PROCESSED_DATA_PATH = "data/processed"
TARGET_COLUMN = "Chance of Admit"
TEST_SIZE = 0.2
RANDOM_STATE = 161



def load_data(path):
    df = pd.read_csv(path)
    df.columns = df.columns.str.strip()
    return df

def clean_split_data(df, target_col, test_size, random_state):
    X = df.drop(columns=["Serial No.",target_col])
    y = df[target_col]
    return train_test_split(X, y, test_size = test_size, random_state = random_state)

def save_data(X_train, X_test, y_train, y_test, output_dir):
    X_train.to_csv(f"{output_dir}/X_train.csv", index=False)
    X_test.to_csv(f"{output_dir}/X_test.csv", index=False)
    y_train.to_csv(f"{output_dir}/y_train.csv", index=False)
    y_test.to_csv(f"{output_dir}/y_test.csv", index=False)

if __name__ == "__main__":
    df = load_data(RAW_DATA_PATH)
    X_train, X_test, y_train, y_test = clean_split_data(df, TARGET_COLUMN, TEST_SIZE, RANDOM_STATE)
    save_data(X_train, X_test, y_train, y_test, PROCESSED_DATA_PATH)
