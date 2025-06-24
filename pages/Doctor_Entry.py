import streamlit as st
from datetime import datetime, timedelta, timezone
from utils.db import get_daily_data, add_data

st.title("Daily Doctor Entry Form")

# Numeric input with built-in number_input
def number_input(label):
    return st.number_input(label, min_value=0, step=1, format="%d")

# Alphabetic input (free text)
def text_input(label):
    return st.text_area(label)

if 'user_id' not in st.session_state:
    st.error("Please login first!")
else:
    last_entry = get_daily_data(st.session_state['user_id'])
    if last_entry and (datetime.now(timezone.utc) - last_entry['timestamp'] < timedelta(hours=24)):
        st.error("Data locked after 24 hours!")
    else:
        st.subheader("Enter Today's Data:")

        # 1. No. of OPD cases
        opd_cases = number_input("1️⃣ No. of OPD cases")

        # 2. No. of procedures done
        procedure_count = number_input("2️⃣ No. of procedures done")

        # 3. Procedure-wise details
        procedure_details = text_input("3️⃣ Procedure-wise details")

        # 4. Whether any surgery performed today?
        surgery_performed = st.radio("4️⃣ Whether any surgery performed today?", ["Yes", "No"])

        # 5. No. of surgeries performed (conditional)
        if surgery_performed == "Yes":
            surgery_count = number_input("5️⃣ No. of surgeries performed")
            surgery_details = text_input("6️⃣ Details of surgeries")
        else:
            surgery_count = 0
            surgery_details = ""

        # Submit button
        if st.button("Submit"):
            if not procedure_details.strip() or (surgery_performed == "Yes" and not surgery_details.strip()):
                st.error("Please fill in all required text fields.")
            else:
                add_data(
                    user_id=st.session_state['user_id'],
                    opd_cases=opd_cases,
                    procedure_count=procedure_count,
                    procedure_details=procedure_details,
                    surgery_performed=surgery_performed,
                    surgery_count=surgery_count,
                    surgery_details=surgery_details
                )
                st.success("Data saved successfully!")
