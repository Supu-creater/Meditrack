import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime, timezone

# Initialize Firebase only once
if not firebase_admin._apps:
    cred = credentials.Certificate("path/to/firebase-credentials.json")  # ← update this path
    firebase_admin.initialize_app(cred)

db = firestore.client()

def add_data(user_id, opd_cases, procedure_count, procedure_details,
             surgery_performed, surgery_count, surgery_details):
    data = {
        "user_id": user_id,
        "timestamp": datetime.now(timezone.utc),
        "opd_cases": opd_cases,
        "procedure_count": procedure_count,
        "procedure_details": procedure_details,
        "surgery_performed": surgery_performed,
        "surgery_count": surgery_count,
        "surgery_details": surgery_details
    }

    # Store in collection "daily_reports"
    db.collection("daily_reports").add(data)
