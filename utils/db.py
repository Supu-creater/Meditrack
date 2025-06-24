import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime

# ✅ Proper Firebase initialization
if not firebase_admin._apps:
    cred = credentials.Certificate(st.secrets["FIREBASE_KEY"])
    firebase_admin.initialize_app(cred)

db = firestore.client()

# ✅ Your existing functions below...
def add_data(user_id, ipd_count, beneficiary_count, receipts, penalty_cases, rsa_patients, aor_patients):
    doc_ref = db.collection("entries").document()
    doc_ref.set({
        "user_id": user_id,
        "ipd_count": ipd_count,
        "beneficiary_count": beneficiary_count,
        "receipts": receipts,
        "penalty_cases": penalty_cases,
        "rsa_patients": rsa_patients,
        "aor_patients": aor_patients,
        "timestamp": datetime.now()
    })

def get_daily_data(user_id):
    docs = db.collection("entries").where("user_id", "==", user_id).stream()
    return max([doc.to_dict() for doc in docs], key=lambda x: x["timestamp"], default=None)

def get_all_data():
    db_ref = firestore.client()
    entries = db_ref.collection("entries").order_by("timestamp", direction=firestore.Query.ASCENDING).stream()
    doctor_docs = db_ref.collection("doctors").stream()
    doctor_map = {doc.id: doc.to_dict() for doc in doctor_docs}

    data = []
    for doc in entries:
        record = doc.to_dict()
        user_id = record.get("user_id", "")
        doctor = doctor_map.get(user_id, {})
        record["email"] = doctor.get("email", "unknown")
        record["name"] = doctor.get("name", "")
        record["unique_code"] = doctor.get("unique_code", "")
        data.append(record)
    return data





