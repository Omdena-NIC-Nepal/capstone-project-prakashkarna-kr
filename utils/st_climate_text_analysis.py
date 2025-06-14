import streamlit as st
import pandas as pd
from typing import Dict, Any
from utils.climate_text_analysis import (
    load_sentiment_data,
    preprocess_data,
    train_sentiment_model,
    save_model,
    load_model,
    clean_text,
)

# Configurable sentiment label mapping at module level
SENTIMENT_LABELS: Dict[int, str] = {1: "Positive", 0: "Negative"}


def display_classification_report(report: Dict[str, Any]):
    """Helper function to display classification report more nicely."""
    st.success(f"Model trained with overall accuracy: {report['accuracy']:.2f}")

    class_metrics_data = {
        SENTIMENT_LABELS.get(int(label), label): metrics
        for label, metrics in report.items()
        if label in ["0", "1"]
    }

    if class_metrics_data:
        class_metrics_df = pd.DataFrame(class_metrics_data).T
        # Ensure correct order of columns if they exist
        cols_to_show = [
            col
            for col in ["precision", "recall", "f1-score", "support"]
            if col in class_metrics_df.columns
        ]
        st.text("Per-Class Metrics:")
        st.table(class_metrics_df[cols_to_show])

    if "macro avg" in report:
        st.text("Macro Average:")
        st.json(report["macro avg"])
    if "weighted avg" in report:
        st.text("Weighted Average:")
        st.json(report["weighted avg"])


def run_climate_text_analysis() -> None:
    st.subheader("Climate Text Sentiment Analysis")

    if "preprocessed_df" not in st.session_state:
        st.session_state.preprocessed_df = None

    if st.button("Load and Preprocess Data"):
        df_loaded: pd.DataFrame = load_sentiment_data()
        df_processed: pd.DataFrame = preprocess_data(df_loaded)
        st.session_state.preprocessed_df = df_processed
        st.success("Data loaded and preprocessed successfully.")
        st.dataframe(df_processed.head())

    if st.button("Train Sentiment Model"):
        df_train: pd.DataFrame = st.session_state.get("preprocessed_df")
        if df_train is not None:
            model, report, _ = train_sentiment_model(
                df_train
            )  # accuracy is part of report
            save_model(model)
            display_classification_report(report)
        else:
            st.warning("Please load and preprocess the data first.")

    st.markdown("---")
    st.subheader("Test the Sentiment Model")

    user_input = st.text_area("Enter a climate-related statement:")
    if st.button("Predict Sentiment"):
        if user_input:
            try:
                model = load_model()
                cleaned_input = clean_text(user_input)
                prediction = model.predict([cleaned_input])[0]
                sentiment: str = SENTIMENT_LABELS.get(
                    prediction, f"Unknown ({prediction})"
                )
                st.write(f"Predicted Sentiment: **{sentiment}**")
            except Exception as e:
                st.error(f"Error: {e}")
        else:
            st.warning("Please enter a statement to analyze.")
