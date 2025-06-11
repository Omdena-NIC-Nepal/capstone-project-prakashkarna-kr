import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
from utils.exploratory import (
    get_basic_stats,
    get_correlation,
    get_time_series,
    get_distribution_data,
)


def run_eda(df):
    st.subheader("Exploratory Data Analysis")

    # Show raw data
    if st.checkbox("Raw Data"):
        with st.container(border=True):
            st.write(df)

    # Show basic stats
    if st.checkbox("Basic Statistics"):
        stats, missing = get_basic_stats(df)
        st.write("Summary Statistics:")
        st.dataframe(stats)
        st.write("Missing Values:")
        st.dataframe(missing)

    # Show correlation heatmap
    if st.checkbox("Correlation Heatmap"):
        with st.container(border=True):
            corr = get_correlation(df)
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.heatmap(corr, annot=True, cmap="coolwarm", ax=ax)
            st.pyplot(fig)

    # Time Series Analysis
    if st.checkbox("Time Series Analysis"):
        date_col = st.selectbox("Select Date Column", df.columns, index=None)
        target_col = st.selectbox(
            "Select Target Column",
            df.select_dtypes(include="number").columns,
            index=None,
        )
        TSA = st.button("GO", type="primary")
        if TSA == True:
            try:
                ts_df = get_time_series(df, date_col, target_col)
                fig, ax = plt.subplots(figsize=(10, 5))
                sns.lineplot(data=ts_df, x=date_col, y=target_col, ax=ax)
                ax.set_title(f"{target_col} over {date_col}")
                st.pyplot(fig)
            except Exception as e:
                st.error(f"Could not generate time series plot: {e}")

    # Distribution Analysis
    if st.checkbox("Distribution Analysis"):
        column = st.selectbox(
            "Select Column for Distribution", df.select_dtypes(include="number").columns
        )
        data = get_distribution_data(df, column)
        fig, ax = plt.subplots()
        sns.histplot(data, kde=True, ax=ax)
        st.pyplot(fig)
