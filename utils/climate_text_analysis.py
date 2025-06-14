import os
import pandas as pd
import joblib
import string
import re
from pathlib import Path
from typing import Tuple, Dict, Any, List

from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, accuracy_score
from sklearn.feature_extraction.text import TfidfVectorizer

DATA_DIR_NAME = "data"
SENTIMENT_DATA_SUBDIR = "sentiment_data"
POSITIVE_CSV = "positive.csv"
NEGATIVE_CSV = "negative.csv"
MODELS_DIR_NAME = "models"
DEFAULT_MODEL_FILENAME = "sentiment_model.pkl"


def load_sentiment_data() -> pd.DataFrame:
    """
    Load positive and negative sentiment data from CSV files.
    Assumes CSVs have a header and a 'Word' column for the text.
    Returns a combined DataFrame with text and corresponding labels.
    """
    try:
        base_dir = Path(__file__).resolve().parent
    except NameError:
        base_dir = Path.cwd()  # Fallback for interactive use
    
    sentiment_data_path = base_dir.parent / DATA_DIR_NAME / SENTIMENT_DATA_SUBDIR
    pos_path = sentiment_data_path / POSITIVE_CSV
    neg_path = sentiment_data_path / NEGATIVE_CSV

    try:
        pos_df_raw = pd.read_csv(pos_path)
        neg_df_raw = pd.read_csv(neg_path)

        if 'Word' not in pos_df_raw.columns:
            raise ValueError(f"Column 'Word' not found in {pos_path}. Expected columns: {pos_df_raw.columns.tolist()}")
        if 'Word' not in neg_df_raw.columns:
            raise ValueError(f"Column 'Word' not found in {neg_path}. Expected columns: {neg_df_raw.columns.tolist()}")

        pos_df = pos_df_raw[['Word']].copy()
        pos_df.rename(columns={'Word': 'text'}, inplace=True)
        
        neg_df = neg_df_raw[['Word']].copy()
        neg_df.rename(columns={'Word': 'text'}, inplace=True)

    except FileNotFoundError as fnf_error:
        raise FileNotFoundError(f"Sentiment data file not found: {fnf_error.filename}. Please check the path.") from fnf_error
    except Exception as e:
        raise ValueError(f"Error processing sentiment CSV files. Ensure they are correctly formatted with a 'Word' column containing text data. Original error: {e}") from e

    pos_df["label"] = 1
    neg_df["label"] = 0

    df = pd.concat([pos_df, neg_df], ignore_index=True)
    df.dropna(subset=["text"], inplace=True)
    df["text"] = df["text"].astype(str)  # Ensure text column is string
    if df.empty:
        raise ValueError("Loaded sentiment data is empty after processing. Check CSV files and 'Word' column content.")
    return df


def clean_text(text: str) -> str:
    """
    Preprocess text by removing punctuation, numbers, and converting to lowercase.
    """
    text = str(text).lower() # Ensure input is string
    text = re.sub(r"\d+", "", text) # Remove numbers
    text = text.translate(str.maketrans("", "", string.punctuation))
    text = text.strip()
    return text


def preprocess_data(df):
    """
    Apply text cleaning to the DataFrame using vectorized string operations for better performance.
    """
    df["clean_text"] = ( # type: ignore
        df["text"]
        .str.lower()
        .str.replace(r"\d+", "", regex=True)
        .str.translate(str.maketrans("", "", string.punctuation))
        .str.strip()
    )
    return df


def train_sentiment_model(df: pd.DataFrame) -> Tuple[Pipeline, Dict[str, Any], float]:
    """
    Train a logistic regression model for sentiment analysis.
    Returns the trained pipeline and evaluation metrics.
    """
    X: pd.Series = df["clean_text"]
    y = df["label"]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    pipeline = Pipeline(
        [
            (
                "tfidf",
                TfidfVectorizer(stop_words="english", ngram_range=(1, 2), min_df=1),
            ),  
            (
                "clf",
                LogisticRegression(solver='liblinear'),
            ),
        ]
    )

    pipeline.fit(X_train, y_train)
    y_pred = pipeline.predict(X_test)

    report = classification_report(y_test, y_pred, output_dict=True)
    accuracy = accuracy_score(y_test, y_pred)

    return pipeline, report, accuracy


def save_model(model: Pipeline, filename: str = DEFAULT_MODEL_FILENAME) -> None:
    """
    Save the trained model to disk.
    """
    try:
        base_dir = Path(__file__).resolve().parent
    except NameError:
        base_dir = Path.cwd()
    model_path = base_dir.parent / MODELS_DIR_NAME / filename
    try:
        model_path.parent.mkdir(parents=True, exist_ok=True)
        joblib.dump(model, model_path)
    except Exception as e:
        raise IOError(f"Failed to save model to {model_path}: {e}")


def load_model(filename: str = DEFAULT_MODEL_FILENAME) -> Pipeline:
    """
    Load the trained model from disk.
    """
    try:
        base_dir = Path(__file__).resolve().parent
    except NameError:
        base_dir = Path.cwd()
    model_path = base_dir.parent / MODELS_DIR_NAME / filename
    return joblib.load(model_path)
