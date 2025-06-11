import os
import joblib
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error, r2_score

def load_model(model_name='linear_regression'):
    """
    Load a trained model from disk.
    """
    model_path = os.path.join(os.path.dirname(__file__), '..', 'models', f"{model_name}.pkl")
    if os.path.exists(model_path):
        return joblib.load(model_path)
    else:
        raise FileNotFoundError(f"Model file {model_path} not found.")

def evaluate_predictions(model, X_test, y_test):
    """
    Evaluate model performance on test data.
    """
    predictions = model.predict(X_test)
    rmse = mean_squared_error(y_test, predictions)
    r2 = r2_score(y_test, predictions)
    return predictions, {'RMSE': rmse, 'R2 Score': r2}

def plot_actual_vs_predicted(y_test, predictions):
    """
    Create a scatter plot of actual vs predicted values.
    """
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.scatter(y_test, predictions, alpha=0.6, edgecolor='k')
    ax.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--')
    ax.set_xlabel("Actual Values")
    ax.set_ylabel("Predicted Values")
    ax.set_title("Actual vs Predicted")
    return fig
