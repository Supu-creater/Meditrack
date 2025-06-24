import streamlit as st
from datetime import datetime, timedelta, timezone
from utils.db import get_daily_data, add_data

st.title("Daily Doctor Entry Form")

def number_input(label):
    return st.number_input(label, min_value=0, step=1, format="%d")

def text_input(label):
    return st.text_area(label)

# Get current user
if 'user_id' not in st.session_state:
    st.error("Please login first!")
else:
    user_id = st.session_state['user_id']
    today = datetime.now(timezone.utc).date()

    # Check if user already submitted today
    last_entry = get_daily_data(user_id)
    if last_entry:
        entry_date = last_entry['timestamp'].astimezone().date()
        if entry_date == today:
            st.warning(f"You have already submitted today’s entry. Last submitted at {last_entry['timestamp'].astimezone().strftime('%Y-%m-%d %H:%M:%S')}")
            st.stop()

    st.subheader("Enter Today's Data:")

    # Auto-fill date
    st.info(f"📅 Date: {today.strftime('%Y-%m-%d')} (auto-filled)")

    opd_cases = number_input("1️⃣ No. of OPD cases")
    procedure_count = number_input("2️⃣ No. of procedures done")
    procedure_details = text_input("3️⃣ Procedure-wise details")
    surgery_performed = st.radio("4️⃣ Whether any surgery performed today?", ["Yes", "No"])

    if surgery_performed == "Yes":
        surgery_count = number_input("5️⃣ No. of surgeries performed")
        surgery_details = text_input("6️⃣ Details of surgeries")
    else:
        surgery_count = 0
        surgery_details = ""

    if st.button("Submit"):
        if not procedure_details.strip() or (surgery_performed == "Yes" and not surgery_details.strip()):
            st.error("Please fill all required text fields.")
        else:
            add_data(
                user_id=user_id,
                opd_cases=opd_cases,
                procedure_count=procedure_count,
                procedure_details=procedure_details,
                surgery_performed=surgery_performed,
                surgery_count=surgery_count,
                surgery_details=surgery_details
            )
            st.success("✅ Data saved successfully!")
