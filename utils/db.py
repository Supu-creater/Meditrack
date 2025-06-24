import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime, timezone

# Initialize Firebase app if not already initialized
if not firebase_admin._apps:
    cred = credentials.Certificate("path/to/firebase-credentials.json")  # Replace with your path
    firebase_admin.initialize_app(cred)

db = firestore.client()

def get_daily_data(user_id):
    """
    Retrieves the latest data entry for the given user_id from Firestore.
    Returns None if no entry exists.
    """
    try:
        docs = db.collection("daily_reports") \
                 .where("user_id", "==", user_id) \
                 .order_by("timestamp", direction=firestore.Query.DESCENDING) \
                 .limit(1) \
                 .stream()

        for doc in docs:
            data = doc.to_dict()
            return data

        return None  # No document found

    except Exception as e:
        print(f"Error fetching daily data for user {user_id}: {e}")
        return None
