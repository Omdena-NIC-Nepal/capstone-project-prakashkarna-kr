import streamlit as st
import pandas as pd
from utils.feature_engineering import (
    handle_missing_values,
    encode_categorical,
    # extract_date_features,
    create_new_feature,
    bin_numerical_variable,
    apply_transformation
)

def run_feature_engineering(df):
    st.subheader("Feature Engineering")

    # Handle missing values
    if st.checkbox("Handle Missing Values"):
        strategy = st.selectbox("Imputation Strategy", ['mean', 'median', 'most_frequent'])
        df = handle_missing_values(df, strategy)
        st.success(f"Missing values handled using {strategy} strategy.")

    # Encode categorical variables
    if st.checkbox("Encode Categorical Variables"):
        df = encode_categorical(df)
        st.success("Categorical variables encoded.")

    # # Extract date features
    # if st.checkbox("Extract Date Features"):
    #     date_column = st.selectbox("Select Date Column", df.columns)
    #     df = extract_date_features(df, date_column)
    #     st.success("Date features extracted.")

    # Create New Feature
    if st.checkbox("Create New Feature"):
        col1 = st.selectbox("Select First Column", df.columns)
        col2 = st.selectbox("Select Second Column", df.columns)
        df = create_new_feature(df, col1, col2)
        st.success(f"Interaction term between {col1} and {col2} created.")

    # Bin numerical variable
    if st.checkbox("Bin Numerical Variable"):
        column = st.selectbox("Select Column to Bin", df.select_dtypes(include='number').columns)
        bins = st.slider("Number of Bins", min_value=2, max_value=10, value=5)
        df = bin_numerical_variable(df, column, bins)
        st.success(f"{column} binned into {bins} intervals.")

    # Apply transformation
    if st.checkbox("Apply Transformation"):
        column = st.selectbox("Select Column to Transform", df.select_dtypes(include='number').columns)
        transformation = st.selectbox("Select Transformation", ['log', 'sqrt'])
        df = apply_transformation(df, column, transformation)
        st.success(f"{transformation} transformation applied to {column}.")

    st.subheader("Transformed Data")
    st.dataframe(df)
