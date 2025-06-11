import streamlit as st

# import seaborn as sns
# import matplotlib.pyplot as plt

from utils.preprocess import load_data
from utils.st_exploratory import run_eda
from utils.st_feature_engineering import run_feature_engineering
from utils.st_model_training import run_model_training
from utils.st_model_evaluation import run_model_evaluation
from utils.st_climate_text_analysis import run_climate_text_analysis


# '''
# root _____________
#         |----------app.py
#         |__________utils
#             |------preprocess.py
#             |------exploratory.py
#             |------st_exploratory.py    #EDA
#             |------feature_engineering.py
#             |------st_feature_engineering.py
#             |------model_training.py
#             |------st_model_training.py
#             |------model_evaluation.py
#             |------st_model_evaluation.py
#             |------prediction.py
#             |------st_prediction.py
#             |------climate_text_analysis.py    # nlp
#             |------st_climate_text_analysis.py


# '''


def main():

    # set page configuration
    st.set_page_config(page_title="Climate Trend Predictor", layout="wide")

    # App title and description
    st.title("Climate Trend Analysis and Prediction")
    st.divider()

    st.markdown("Analyse historical tempreature and predict trend")


    # side bar

    st.sidebar.title("Navigation Page")
    page = st.sidebar.radio(
        "Go to",
        [
            "EDA",
            "Feature Engineering",
            "Model Training",
            "Model Evaluation",
            "Climate Text Analysis",
        ],
    )

    # if 'df' not in st.session_state:
    #     st.session_state.df = load_data()

    # df = st.session_state.df
    df = load_data()
    try:
        if page == "EDA":
            run_eda(df)  # call EDA part

        elif page == "Feature Engineering":
            df = run_feature_engineering(df)

        elif page == "Model Training":
            run_model_training(df)

        elif page == "Model Evaluation":
            run_model_evaluation(df)

        else:
            run_climate_text_analysis()

    except Exception as e:
        st.error(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
