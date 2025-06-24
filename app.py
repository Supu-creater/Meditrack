import streamlit as st
from datetime import datetime, timezone
from utils.db import get_daily_data, add_data

st.set_page_config(page_title="Doctor Daily Report", layout="centered")
st.title("🩺 Daily Doctor Entry Form")

# Ensure user is logged in
if 'user_id' not in st.session_state:
    st.error("⚠️ Please login to access this form.")
    st.stop()

user_id = st.session_state['user_id']
today = datetime.now(timezone.utc).date()

# Check if already submitted today
last_entry = get_daily_data(user_id)
if last_entry:
    entry_date = last_entry['timestamp'].astimezone(timezone.utc).date()
    if entry_date == today:
        st.warning("✅ You have already submitted today’s report.")
        st.info(f"🕒 Last submitted at: {last_entry['timestamp'].astimezone().strftime('%Y-%m-%d %H:%M:%S')}")
        st.stop()

# Show today's date
st.markdown(f"📅 **Date:** `{today.strftime('%Y-%m-%d')}` _(auto-filled)_")

# ---- FORM UI ---- #
with st.form("doctor_form"):
    opd_cases = st.number_input("1️⃣ No. of OPD cases", min_value=0, step=1)
    procedure_count = st.number_input("2️⃣ No. of procedures done", min_value=0, step=1)
    procedure_details = st.text_area("3️⃣ Procedure-wise details (short para)")

    surgery_performed = st.radio("4️⃣ Whether any surgery performed today?", ["Yes", "No"])

    if surgery_performed == "Yes":
        surgery_count = st.number_input("5️⃣ No. of surgeries performed", min_value=0, step=1)
        surgery_details = st.text_area("6️⃣ Details of surgeries")
    else:
        surgery_count = 0
        surgery_details = ""

    submitted = st.form_submit_button("Submit Report")

# ---- FORM HANDLER ---- #
if submitted:
    if not procedure_details.strip():
        st.error("❌ Please enter procedure-wise details.")
    elif surgery_performed == "Yes" and not surgery_details.strip():
        st.error("❌ Please enter details of surgeries performed.")
    else:
        add_data(
            user_id=user_id,
            opd_cases=opd_cases,
            procedure_count=procedure_count,
            procedure_details=procedure_details.strip(),
            surgery_performed=surgery_performed,
            surgery_count=surgery_count,
            surgery_details=surgery_details.strip()
        )
        st.success("✅ Your daily report has been submitted successfully!")
