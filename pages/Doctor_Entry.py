import streamlit as st
from datetime import datetime, timezone
from utils.db import get_daily_data, add_data

st.set_page_config(page_title="Doctor Report")
st.title("🩺 Daily Doctor Entry Form")

# Mock login for testing
if 'user_id' not in st.session_state:
    st.session_state['user_id'] = st.text_input("Enter Doctor Code to continue")
    st.stop()

user_id = st.session_state['user_id']
today = datetime.now(timezone.utc).date()

# Check if already submitted
last_entry = get_daily_data(user_id)
if last_entry:
    ts = last_entry.get("timestamp")
    if ts and ts.astimezone().date() == today:
        st.warning("✅ You’ve already submitted today’s report.")
        st.info(f"🕒 Last submitted at: {ts.astimezone().strftime('%Y-%m-%d %H:%M:%S')}")
        st.stop()

st.subheader("Enter Today's Data")
st.info(f"📅 Date: {today.strftime('%Y-%m-%d')} (auto-filled)")

opd_cases = st.number_input("1️⃣ No. of OPD cases", min_value=0, step=1)
procedure_count = st.number_input("2️⃣ No. of procedures done", min_value=0, step=1)
procedure_details = st.text_area("3️⃣ Procedure-wise details")

surgery_performed = st.radio("4️⃣ Any surgery today?", ["Yes", "No"])
if surgery_performed == "Yes":
    surgery_count = st.number_input("5️⃣ No. of surgeries performed", min_value=0, step=1)
    surgery_details = st.text_area("6️⃣ Details of surgeries")
else:
    surgery_count = 0
    surgery_details = ""

if st.button("Submit"):
    if not procedure_details.strip() or (surgery_performed == "Yes" and not surgery_details.strip()):
        st.error("Please fill all required fields.")
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
