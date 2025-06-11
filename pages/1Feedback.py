import streamlit as st
import pandas as pd

# Initialize session state
if "feedback_form_submitted" not in st.session_state:
    st.session_state.feedback_form_submitted = False

if not st.session_state.feedback_form_submitted:
    st.title("Your feedback will be highly appriceated!")
    st.divider()

    feedback = st.text_input("Drop your feedback here")
    f_name = st.text_input("Drop your name here")
    f_email = st.text_input("Drop your Email-Id here")
    f_rateing = st.slider("Select your rating", 0, 10)

    # Display the summary table
    if f_name or f_email or feedback:  # Check if any field has input
        f_data = pd.DataFrame(
            {
                "Field": ["Name", "Email", "Rating", "Feedback"],
                "Response": [f_name, f_email, f_rateing, feedback],
            }
        )
        html_data = f_data.to_html(index=False, header=False)
        st.markdown(html_data, unsafe_allow_html=True)

    if st.button("Submit Now"):
        st.session_state.feedback_form_submitted = True
        st.balloons()
        st.image("pages/assets/thank_you_image.png")
        st.rerun()

elif st.session_state.feedback_form_submitted:
    st.balloons()
    st.image("pages/assets/thank_you_image.png")
