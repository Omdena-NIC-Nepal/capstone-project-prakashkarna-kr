import streamlit as st
from utils.model_evaluation import load_model, evaluate_predictions, plot_actual_vs_predicted
from utils.preprocess import preprocess_data

def run_model_evaluation(df):
    st.subheader("📊 Model Evaluation")

    target_col = st.selectbox("Select Target Column", df.columns)

    model_name = st.selectbox("Select Trained Model", ["linear_regression", "random_forest"])

    # Preprocess data
    X_train, X_test, y_train, y_test, _ = preprocess_data(df, target_col)

    try:
        model = load_model(model_name)
        predictions, metrics = evaluate_predictions(model, X_test, y_test)

        st.write("### Evaluation Metrics")
        st.write(metrics)

        st.write("### Actual vs Predicted Plot")
        fig = plot_actual_vs_predicted(y_test, predictions)
        st.pyplot(fig)

    except FileNotFoundError as e:
        st.error(str(e))
