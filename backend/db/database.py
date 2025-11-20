import os
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

# -------------------------------------------------
# MongoDB connection (Docker / Local by default)
# -------------------------------------------------
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")

try:
    client = MongoClient(MONGO_URI)
    db = client["veinpay_db"]
    users_collection = db["users"]
    print("[MongoDB via Docker] Connected successfully!")
except ConnectionFailure as e:
    print("[MongoDB] Connection failed:", e)
    raise e


# -------------------------------------------------
# Save / update user embedding (averaged)
# -------------------------------------------------
def save_user_embedding(user_id: str, embedding, sample_count: int, avg_quality: float):
    """
    Stores or updates the averaged embedding for a user.

    :param user_id: unique user identifier (string)
    :param embedding: list/array of floats
    :param sample_count: number of samples used to compute this embedding
    :param avg_quality: average skeleton quality across samples
    """
    users_collection.update_one(
        {"user_id": user_id},
        {
            "$set": {
                "user_id": user_id,
                "embedding": embedding,
                "sample_count": sample_count,
                "avg_quality": avg_quality,
            }
        },
        upsert=True,
    )


# -------------------------------------------------
# Retrieve stored embedding
# -------------------------------------------------
def get_user_embedding(user_id: str):
    """
    Returns stored embedding array for user_id, or None if not found.
    """
    doc = users_collection.find_one({"user_id": user_id})
    if not doc:
        return None
    return doc.get("embedding")
