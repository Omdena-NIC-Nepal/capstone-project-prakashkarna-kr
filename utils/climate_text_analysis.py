import os
import pandas as pd
import numpy as np
import joblib
import string
import re

from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, accuracy_score
from sklearn.feature_extraction.text import TfidfVectorizer

def load_sentiment_data():
    """
    Load positive and negative sentiment data from CSV files.
    Returns a combined DataFrame with text and corresponding labels.
    """
    base_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'sentiment_data')
    pos_path = os.path.join(base_path, 'positive.csv')
    neg_path = os.path.join(base_path, 'negative.csv')

    pos_df = pd.read_csv(pos_path, header=None, names=['text'])
    neg_df = pd.read_csv(neg_path, header=None, names=['text'])

    pos_df['label'] = 1
    neg_df['label'] = 0

    df = pd.concat([pos_df, neg_df], ignore_index=True)
    df.dropna(subset=['text'], inplace=True)
    return df

def clean_text(text):
    """
    Preprocess text by removing punctuation, numbers, and converting to lowercase.
    """
    text = text.lower()
    text = re.sub(r'\d+', '', text)
    text = text.translate(str.maketrans('', '', string.punctuation))
    text = text.strip()
    return text

def preprocess_data(df):
    """
    Apply text cleaning to the DataFrame.
    """
    df['clean_text'] = df['text'].apply(clean_text)
    return df

def train_sentiment_model(df):
    """
    Train a logistic regression model for sentiment analysis.
    Returns the trained pipeline and evaluation metrics.
    """
    X = df['clean_text']
    y = df['label']

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    pipeline = Pipeline([
        ('tfidf', TfidfVectorizer(stop_words='english')),
        ('clf', LogisticRegression(solver='liblinear'))
    ])

    pipeline.fit(X_train, y_train)
    y_pred = pipeline.predict(X_test)

    report = classification_report(y_test, y_pred, output_dict=True)
    accuracy = accuracy_score(y_test, y_pred)

    return pipeline, report, accuracy

def save_model(model, filename='sentiment_model.pkl'):
    """
    Save the trained model to disk.
    """
    model_path = os.path.join(os.path.dirname(__file__), '..', 'models', filename)
    os.makedirs(os.path.dirname(model_path), exist_ok=True)
    joblib.dump(model, model_path)

def load_model(filename='sentiment_model.pkl'):
    """
    Load a trained model from disk.
    """
    model_path = os.path.join(os.path.dirname(__file__), '..', 'models', filename)
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model file not found at {model_path}")
    return joblib.load(model_path)
