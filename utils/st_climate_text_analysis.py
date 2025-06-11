import streamlit as st
from utils.climate_text_analysis import (
    load_sentiment_data,
    preprocess_data,
    train_sentiment_model,
    save_model,
    load_model,
    clean_text
)

def run_climate_text_analysis():
    st.subheader("Climate Text Sentiment Analysis")

    if st.button("Load and Preprocess Data"):
        df = load_sentiment_data()
        df = preprocess_data(df)
        st.success("Data loaded and preprocessed successfully.")
        st.dataframe(df.head())

    if st.button("Train Sentiment Model"):
        df = load_sentiment_data()
        df = preprocess_data(df)
        model, report, accuracy = train_sentiment_model(df)
        save_model(model)
        st.success(f"Model trained with accuracy: {accuracy:.2f}")
        st.text("Classification Report:")
        st.json(report)

    st.markdown("---")
    st.subheader("Test the Sentiment Model")

    user_input = st.text_area("Enter a climate-related statement:")
    if st.button("Predict Sentiment"):
        if user_input:
            try:
                model = load_model()
                cleaned_input = clean_text(user_input)
                prediction = model.predict([cleaned_input])[0]
                sentiment = "Positive" if prediction == 1 else "Negative"
                st.write(f"Predicted Sentiment: **{sentiment}**")
            except Exception as e:
                st.error(f"Error: {e}")
        else:
            st.warning("Please enter a statement to analyze.")
