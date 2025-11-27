import os
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from dotenv import load_dotenv

# -------------------------------------------------
# Load .env file (if present)
# -------------------------------------------------
load_dotenv()

# -------------------------------------------------
# MongoDB connection URI — NOT HARD-CODED
# -------------------------------------------------

# First priority: environment variable from .env
MONGO_URI = os.getenv("MONGO_URI")

# Fallback: local Docker container
if not MONGO_URI:
    MONGO_URI = "mongodb://localhost:27017/"

print(f"[MongoDB] Using URI: {MONGO_URI}")

# -------------------------------------------------
# Connect to MongoDB
# -------------------------------------------------
try:
    client = MongoClient(MONGO_URI)
    db = client["veinpay_db"]
    users_collection = db["users"]
    print("[MongoDB] Connected successfully!")
except ConnectionFailure as e:
    print("[MongoDB] Connection failed:", e)
    raise e


# -------------------------------------------------
# Save / update embedding
# -------------------------------------------------
def save_user_embedding(user_id: str, embedding):
    """
    Stores the embedding for a single-image registration.
    """

    users_collection.update_one(
        {"user_id": user_id},
        {
            "$set": {
                "user_id": user_id,
                "embedding": embedding,
            }
        },
        upsert=True,
    )


# -------------------------------------------------
# Retrieve embedding
# -------------------------------------------------
def get_user_embedding(user_id: str):
    """
    Returns embedding array for user_id, or None.
    """
    doc = users_collection.find_one({"user_id": user_id})
    if not doc:
        return None
    return doc.get("embedding")
