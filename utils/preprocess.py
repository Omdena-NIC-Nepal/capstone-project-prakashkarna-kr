import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import joblib
import streamlit as st

# Cache the data to prevent reloading
@st.cache_data
def load_data(file_path=None):
    """Load the climate dataset from CSV."""
    if file_path is None:
        file_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'processed_data.csv')
    
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"No data file found at: {file_path}")

    data = pd.read_csv(file_path)
    data['year'] = data['year'].astype(int)  # ensure 'year' is integer
    return data

def preprocess_data(data, target_col='avg_max_temp', test_size=0.2, random_state=42):
    """Split data and scale numeric features."""
    X = data.drop(columns=[target_col])
    y = data[target_col]

    # Split into train and test sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)

    # Scale only numeric columns
    scaler = StandardScaler()
    num_cols = X_train.select_dtypes(include='number').columns
    X_train[num_cols] = scaler.fit_transform(X_train[num_cols])
    X_test[num_cols] = scaler.transform(X_test[num_cols])

    return X_train, X_test, y_train, y_test, scaler

def save_model(model, model_name):
    """Save a model to disk."""
    model_dir = os.path.join(os.path.dirname(__file__), '..', 'models')
    os.makedirs(model_dir, exist_ok=True)
    joblib.dump(model, os.path.join(model_dir, f"{model_name}.pkl"))

def load_model(model_name):
    """Load a saved model."""
    model_path = os.path.join(os.path.dirname(__file__), '..', 'models', f"{model_name}.pkl")
    
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model '{model_name}' not found.")
    
    return joblib.load(model_path)
