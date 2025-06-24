import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime, timezone

# Initialize Firebase app (only once)
if not firebase_admin._apps:
    cred = credentials.Certificate("firebase-creds.json")  # ← Update with your actual filename
    firebase_admin.initialize_app(cred)

# Firestore client
db = firestore.client()

def get_daily_data(user_id):
    """
    Fetches the latest daily report for the user.
    Returns the report dict if it was submitted today, else None.
    """
    try:
        # Get the most recent document for the user
        docs = db.collection("daily_reports") \
                 .where("user_id", "==", user_id) \
                 .order_by("timestamp", direction=firestore.Query.DESCENDING) \
                 .limit(1) \
                 .stream()

        for doc in docs:
            data = doc.to_dict()

            # Convert timestamp to date (UTC)
            entry_time = data.get("timestamp")
            if entry_time is not None:
                today = datetime.now(timezone.utc).date()
                entry_date = entry_time.astimezone(timezone.utc).date()

                if entry_date == today:
                    return data  # Entry for today exists

        return None  # No entry found for today

    except Exception as e:
        print(f"Error fetching daily data for {user_id}: {e}")
        return None
