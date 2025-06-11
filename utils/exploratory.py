import pandas as pd
import numpy as np

def get_basic_stats(df):
    """Return basic statistics and missing values info."""
    summary = df.describe()
    missing = df.isnull().sum()
    return summary, missing

def get_correlation(df):
    """Return correlation matrix."""
    return df.corr()

def get_time_series(df, date_col, target_col):
    """Return data for simple time series lineplot without datetime parsing."""
    ts_df = df[[date_col, target_col]].dropna().copy()

    # If date_col is numeric like 'year', skip datetime conversion
    if not np.issubdtype(df[date_col].dtype, np.datetime64):
        ts_df = ts_df.sort_values(by=date_col)
    else:
        ts_df[date_col] = pd.to_datetime(ts_df[date_col], errors='raise')
        ts_df = ts_df.sort_values(by=date_col)

    return ts_df



def get_distribution_data(df, column):
    """Return data for distribution analysis."""
    return df[column].dropna()
