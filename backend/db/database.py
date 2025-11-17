from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

# ----------------------------------------
# HARDCODE YOUR MONGO ATLAS URI HERE
# ----------------------------------------
# Replace the string below with your actual Atlas connection URI

MONGO_URI = "mongodb+srv://nikhilanand:060O47HDut2eWPEa@veinpay.xw80fkf.mongodb.net"
if not MONGO_URI:
    raise Exception("MONGO_URI is empty! Add your Atlas connection string.")

# ----------------------------------------
# Connect to MongoDB Atlas
# ----------------------------------------
try:
    client = MongoClient(MONGO_URI)
    db = client["veinpay_db"]             # Database name
    users_collection = db["users"]        # Collection
    print("[MongoDB Atlas] Connected successfully!")

except ConnectionFailure as e:
    print("[MongoDB Atlas] Connection failed:", e)
    raise e


# ----------------------------------------
# Save / Update User Signature
# ----------------------------------------
def save_user_signature(user_id: str, signature: str):
    """
    Stores or updates the user's biometric signature.
    """
    users_collection.update_one(
        {"user_id": user_id},
        {"$set": {"signature": signature}},
        upsert=True
    )
    print(f"[MongoDB] Signature stored for user: {user_id}")


# ----------------------------------------
# Get User Signature
# ----------------------------------------
def get_user_signature(user_id: str):
    """
    Retrieves stored signature. Returns None if not found.
    """
    user = users_collection.find_one({"user_id": user_id})
    if user:
        return user.get("signature")
    print(f"[MongoDB] No signature found for user: {user_id}")
    return None
