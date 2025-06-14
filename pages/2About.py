import streamlit as st
import base64
import os


def get_base64_of_bin_file(bin_file):
    """
    Function to convert binary file to base64 string.
    """
    with open(bin_file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()


def set_page_background(png_file):
    """
    Function to set the background of a Streamlit page.
    """
    bin_str = get_base64_of_bin_file(png_file)
    page_bg_img = f"""
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{bin_str}");
        background-size: cover;
    }}
    </style>
    """
    st.markdown(page_bg_img, unsafe_allow_html=True)


st.title("About This Project")
st.divider()
st.header(
    "Develop an end-to-end data analysis system that monitors, analyzes, and predicts climate change impacts in Nepal with a focus on vulnerable regions"
)

image_path = "pages/assets/about_background.png"

if os.path.exists(image_path):
    set_page_background(image_path)
else:
    st.warning(f"Background image not found at {image_path}. Please check the path.")
