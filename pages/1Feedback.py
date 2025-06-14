import streamlit as st
import pandas as pd
import time # Import the time module
import gspread
from google.oauth2.service_account import Credentials
import os
from datetime import datetime

if "form_needs_reset" not in st.session_state:
    st.session_state.form_needs_reset = False

if st.session_state.form_needs_reset:
    st.session_state.feedback_text_input = ""
    st.session_state.feedback_name_input = ""
    st.session_state.feedback_email_input = ""
    st.session_state.feedback_rating_slider = 0  
    st.session_state.form_needs_reset = False 

st.title("Your feedback will be highly appriceated!")
st.divider()

GOOGLE_SHEET_NAME = "Feedback_Capstone"
GOOGLE_SHEET_WORKSHEET_NAME = "Sheet1"

LOCAL_GOOGLE_CREDENTIALS_PATH = "google_credentials.json" 



def get_gspread_client():
    """Authenticates with Google Sheets API and returns a gspread client."""
    scopes = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
    client = None # Initialize client to None

    try:
        if hasattr(st, 'secrets') and st.secrets:
            creds_dict = st.secrets.get("gcp_service_account")
            if creds_dict:
                print(f"DEBUG: Attempting to use st.secrets['gcp_service_account']. Type: {type(creds_dict)}")
                client = gspread.service_account_from_dict(creds_dict, scopes=scopes)
                print("DEBUG: Client initialized from st.secrets.")
            else:
                print("DEBUG: 'gcp_service_account' key not found in st.secrets.")
        else:
            print("DEBUG: st.secrets not available or empty, assuming local development or misconfiguration.")
            
    except Exception as e: 
        print(f"DEBUG: Error initializing client from st.secrets: {e}. Will try local file.")
        client = None 

    if client is None: 
        if os.path.exists(LOCAL_GOOGLE_CREDENTIALS_PATH):
            print(f"DEBUG: Found local credentials at: {os.path.abspath(LOCAL_GOOGLE_CREDENTIALS_PATH)}")
            try:
                client = gspread.service_account(filename=LOCAL_GOOGLE_CREDENTIALS_PATH, scopes=scopes)
                print("DEBUG: Client initialized from local file.")
            except Exception as e:
                print(f"DEBUG: Error initializing client from local file {LOCAL_GOOGLE_CREDENTIALS_PATH}: {e}")
                st.error(f"Failed to initialize Google Sheets client from local file: {e}")
                return None
        else:
            st.error("Google Sheets credentials not found. Please configure them for deployment in .streamlit/secrets.toml or ensure 'google_credentials.json' is in the project root for local development.")
            return None
    
    if client is None:
        st.error("Failed to initialize Google Sheets client through any method.")
        return None
        
    return client


def append_to_google_sheet(client, sheet_name, worksheet_name, data_row: list):
    """Appends a data row to the specified Google Sheet. Adds header if not present."""
    try:
        sheet = client.open(sheet_name).worksheet(worksheet_name)
        header = ["Timestamp", "Name", "Email", "Rating", "Feedback"]
        if not sheet.get_all_values() or sheet.row_values(1) != header: 
             sheet.insert_row(header, 1) 
        sheet.append_row(data_row) 
        return True
    except Exception as e:
        st.error(f"Failed to append data to Google Sheet: {e}")
        return False

feedback = st.text_input("Drop your feedback here", key="feedback_text_input")
f_name = st.text_input("Drop your name here", key="feedback_name_input")
f_email = st.text_input("Drop your Email-Id here", key="feedback_email_input")
f_rateing = st.slider("Select your rating", 0, 10, key="feedback_rating_slider")

if f_name or f_email or feedback:  
    f_data = pd.DataFrame(
        {
            "Field": ["Name", "Email", "Rating", "Feedback"],
            "Response": [f_name, f_email, f_rateing, feedback],
        }
    )
    html_data = f_data.to_html(index=False, header=False)
    st.markdown(html_data, unsafe_allow_html=True)

all_fields_filled = bool(feedback and f_name and f_email)

if st.button("Submit Now", disabled=not all_fields_filled):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data_to_save = [timestamp, f_name, f_email, f_rateing, feedback]

    gspread_client = get_gspread_client()
    if gspread_client:
        if append_to_google_sheet(gspread_client, GOOGLE_SHEET_NAME, GOOGLE_SHEET_WORKSHEET_NAME, data_to_save):
            st.success("Feedback submitted successfully and saved!")
            st.balloons()
            st.image("pages/assets/thank_you_image.png")
            
            with st.empty(): 
                for i in range(5, 0, -1):
                    st.info(f"Resetting form in {i} seconds...")
                    time.sleep(1)
            
            st.session_state.last_feedback_submission_time = time.time() 
            st.session_state.form_needs_reset = True 
            
            st.rerun()
        else:
            st.error("Failed to save feedback. Please try again or contact support.")
