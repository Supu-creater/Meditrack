import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime, timezone

# Initialize Firebase only once
if not firebase_admin._apps:
    cred = credentials.Certificate("firebase-creds.json")  # 🔁 Change path if needed
    firebase_admin.initialize_app(cred)

# Firestore client
db = firestore.client()

def add_data(user_id, opd_cases, procedure_count, procedure_details,
             surgery_performed, surgery_count, surgery_details):
    """
    Adds a new daily report entry to Firestore.
    """
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

    db.collection("daily_reports").add(data)


def get_daily_data(user_id):
    """
    Fetches the latest daily report for the user.
    Returns the report if it's from today; else None.
    """
    try:
        docs = db.collection("daily_reports") \
                 .where("user_id", "==", user_id) \
                 .order_by("timestamp", direction=firestore.Query.DESCENDING) \
                 .limit(1) \
                 .stream()

        for doc in docs:
            data = doc.to_dict()
            timestamp = data.get("timestamp")
            if timestamp:
                today = datetime.now(timezone.utc).date()
                entry_date = timestamp.astimezone(timezone.utc).date()
                if entry_date == today:
                    return data
        return None

    except Exception as e:
        print(f"⚠️ Error fetching daily data for {user_id}: {e}")
        return None
