import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import joblib
import os



def train_model(X_train, y_train, model_type='Linear Regression', **kwargs):
    #Train a machine learning model based on the specified type.

    if model_type == 'Linear Regression':
        model = LinearRegression(**kwargs)
    elif model_type == 'Random Forest':
        model = RandomForestRegressor(**kwargs)
    else:
        raise ValueError(f"Unsupported model type: {model_type}")

    model.fit(X_train, y_train)
    return model

def evaluate_model(model, X_test, y_test):

    #Evaluate the trained model using test data.

    predictions = model.predict(X_test)
    rmse = mean_squared_error(y_test, predictions)
    r2 = r2_score(y_test, predictions)
    return {'RMSE': rmse, 'R2 Score': r2}

def save_model(model, model_name='trained_model'):
    """
    Save the trained model.

    
    """
    models_dir = os.path.join(os.path.dirname(__file__), '..', 'models')
    os.makedirs(models_dir, exist_ok=True)
    model_path = os.path.join(models_dir, f"{model_name}.pkl")
    joblib.dump(model, model_path)
