import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder
from sklearn.impute import SimpleImputer

def handle_missing_values(df, strategy='mean'):
    """Impute missing values using the specified strategy."""
    imputer = SimpleImputer(strategy=strategy)
    numeric_cols = df.select_dtypes(include=np.number).columns
    df[numeric_cols] = imputer.fit_transform(df[numeric_cols])
    return df

def encode_categorical(df):
    """One-hot encode categorical variables."""
    categorical_cols = df.select_dtypes(include='object').columns
    df = pd.get_dummies(df, columns=categorical_cols, drop_first=True)
    return df

# def extract_date_features(df, date_col):
#     df[date_col] = pd.to_datetime(df[date_col], errors='coerce')
#     df['year'] = df[date_col].dt.year
#     df['month'] = df[date_col].dt.month
#     df['day'] = df[date_col].dt.day
#     df['day_of_week'] = df[date_col].dt.dayofweek
#     df['week_of_year'] = df[date_col].dt.isocalendar().week.astype(int)
#     df['is_weekend'] = df[date_col].dt.dayofweek >= 5
#     df['quarter'] = df[date_col].dt.quarter
#     return df

def create_new_feature(df, col1, col2):
    """Create interaction term between two columns."""
    df[f'{col1}_x_{col2}'] = df[col1] * df[col2]
    return df

def bin_numerical_variable(df, column, bins=5, labels=None):
    """Bin a numerical variable into discrete intervals."""
    df[f'{column}_binned'] = pd.cut(df[column], bins=bins, labels=labels)
    return df

def apply_transformation(df, column, transformation='log'):
    """Apply a mathematical transformation to a column."""
    if transformation == 'log':
        df[f'{column}_log'] = np.log1p(df[column])
    elif transformation == 'sqrt':
        df[f'{column}_sqrt'] = np.sqrt(df[column])
    return df
