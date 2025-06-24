def get_daily_data(user_id):
    from firebase_admin import firestore
    db = firestore.client()
    
    docs = db.collection("daily_reports") \
             .where("user_id", "==", user_id) \
             .order_by("timestamp", direction=firestore.Query.DESCENDING) \
             .limit(1) \
             .stream()
    
    for doc in docs:
        return doc.to_dict()
    return None
