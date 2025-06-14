import streamlit as st
from utils.model_training import train_model, evaluate_model, save_model
from utils.preprocess import preprocess_data

def run_model_training(df):
    st.subheader("Model Training")

    # Select target variable
    target_col = st.selectbox("Select Target Variable", df.columns)

    # Split and preprocess data
    X_train, X_test, y_train, y_test, scaler = preprocess_data(df, target_col=target_col)

    # Select model type
    model_type = st.selectbox("Select Model Type", ['Linear Regression', 'Random Forest'])

    # Set model parameters
    params = dict()
    if model_type == 'Random Forest':
        n_estimators = st.slider("Number of Trees", 10, 100, 50)
        max_depth = st.slider("Maximum Depth", 1, 20, 5)
        params['n_estimators'] = n_estimators
        params['max_depth'] = max_depth

    # Train model
    if st.button("Train Model"):
        model = train_model(X_train, y_train, model_type=model_type, **params)
        metrics = evaluate_model(model, X_test, y_test)
        st.write("Model Evaluation Metrics:")
        st.write(metrics)

        # Predict
        # y_pred = model.predict(X_test)

        # Save model
        save_model(model, model_name=model_type.replace(" ", "_").lower())
        # st.session_state.trained_model = model
        # st.session_state.model_name = model_type
        # st.session_state.X_test = X_test
        # st.session_state.y_test = y_test
        # st.session_state.y_pred = y_pred
        st.success(f"{model_type} model trained and saved successfully.")
