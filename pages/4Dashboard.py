import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
import os

st.title("Dashboard")
st.divider()

# --- Google Sheets Configuration (same as in 1Feedback.py) ---
GOOGLE_SHEET_NAME = "Feedback_Capstone"  
GOOGLE_SHEET_WORKSHEET_NAME = "Sheet1"     
LOCAL_GOOGLE_CREDENTIALS_PATH = "google_credentials.json"

def get_gspread_client():
    """Authenticates with Google Sheets API and returns a gspread client."""
    scopes = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
    client = None # Initialize client to None

    try:
        if hasattr(st, 'secrets') and st.secrets:
            creds_dict = st.secrets.get("gcp_service_account") # Use .get() for safer access
            if creds_dict:
                print(f"DEBUG: Attempting to use st.secrets['gcp_service_account']. Type: {type(creds_dict)}")
                client = gspread.service_account_from_dict(creds_dict, scopes=scopes)
                print("DEBUG: Client initialized from st.secrets.")
            else:
                print("DEBUG: 'gcp_service_account' key not found in st.secrets.")
        else:
            print("DEBUG: st.secrets not available or empty, assuming local development or misconfiguration.")
            
    except Exception as e: # Catch any error during secrets processing or gspread init
        print(f"DEBUG: Error initializing client from st.secrets: {e}. Will try local file.")
        client = None # Ensure client is None if secrets method failed

    # Fallback to local JSON file (for local development)
    if client is None: # Only try local file if client wasn't initialized from secrets
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
            # This error will be shown if neither secrets nor local file worked
            st.error("Google Sheets credentials not found. Please configure them for deployment in .streamlit/secrets.toml or ensure 'google_credentials.json' is in the project root for local development.")
            return None
    
    # If client is still None here, it means both methods failed.
    if client is None:
        st.error("Failed to initialize Google Sheets client through any method.")
        return None
        
    return client


@st.cache_data(ttl=600) # Cache data
def read_all_feedback_data(_client, sheet_name, worksheet_name, refresh_trigger=None) -> pd.DataFrame | None:
    """Reads all data from the specified Google Sheet worksheet and returns a DataFrame."""
    if not _client:
        return None
    try:
        sheet = _client.open(sheet_name).worksheet(worksheet_name)
        data = sheet.get_all_records()  
        if not data:
            return pd.DataFrame() #
        df = pd.DataFrame(data)
        if 'Rating' in df.columns:
            df['Rating'] = pd.to_numeric(df['Rating'], errors='coerce')
        return df 
    except gspread.exceptions.SpreadsheetNotFound:
        st.error(f"Spreadsheet '{sheet_name}' not found. Please check the name and sharing permissions.")
        return None
    except gspread.exceptions.WorksheetNotFound:
        st.error(f"Worksheet '{worksheet_name}' not found in '{sheet_name}'.")
        return None
    except Exception as e:
        st.error(f"Failed to read data from Google Sheet: {e}")
        return None

# Create tabs
tab1, tab2 = st.tabs(["👨‍🏫 Feedback", "📊 Ratings"])

with tab1:
   st.header("You can find Feedbacks Here")
   
   options = ["All Feedback", "Positive Ratings (Rating > 5)", "Negative Ratings (Rating <= 5)"]
   filter_option = st.selectbox(
       "Filter feedback by:",
       options,
       index=0 # Default to "All Feedback"
   )

   g_client = get_gspread_client()
   if g_client:
       last_submission_time = st.session_state.get("last_feedback_submission_time", 0)
       feedback_df = read_all_feedback_data(
           g_client, GOOGLE_SHEET_NAME, GOOGLE_SHEET_WORKSHEET_NAME,
           refresh_trigger=last_submission_time
       )
       
       if feedback_df is not None:
           if not feedback_df.empty:
                display_df = feedback_df.copy() 

                if 'Rating' not in display_df.columns:
                    st.warning("The 'Rating' column is missing from the feedback data. Cannot filter by rating.")
                elif filter_option == options[1]: # Positive Ratings
                    display_df = display_df[display_df['Rating'] > 5]
                elif filter_option == options[2]: # Negative Ratings
                    display_df = display_df[display_df['Rating'] <= 5]

                if not display_df.empty:
                    st.dataframe(display_df)
                else:
                    st.info(f"No feedback entries found for the selected filter: '{filter_option}'.")
           else:
               st.info("No feedback data found in the sheet yet.")


with tab2:
   st.header("Feedback Ratings Distribution")
   
   g_client_tab2 = get_gspread_client()
   if g_client_tab2:
       last_submission_time_tab2 = st.session_state.get("last_feedback_submission_time", 0)
       feedback_df_tab2 = read_all_feedback_data(
           g_client_tab2, GOOGLE_SHEET_NAME, GOOGLE_SHEET_WORKSHEET_NAME,
           refresh_trigger=last_submission_time_tab2
       )

       if feedback_df_tab2 is not None and not feedback_df_tab2.empty:
           if 'Rating' in feedback_df_tab2.columns:
               rating_counts = feedback_df_tab2['Rating'].value_counts().sort_index()
               if not rating_counts.empty:
                   fig, ax = plt.subplots()
                   ax.pie(rating_counts, labels=rating_counts.index, autopct='%1.1f%%', startangle=90)
                   ax.axis('equal')  
                   st.pyplot(fig)
               else:
                   st.info("No ratings available to display in the pie chart.")
           else:
               st.warning("The 'Rating' column is missing from the feedback data.")
       elif feedback_df_tab2 is not None and feedback_df_tab2.empty:
            st.info("No feedback data found in the sheet yet to display ratings.")