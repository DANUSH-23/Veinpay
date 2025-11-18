import os
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from dotenv import load_dotenv

# ----------------------------------------
# Load environment variables from .env
# ----------------------------------------
load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

if not MONGO_URI:
    raise Exception(
        "MONGO_URI is not set. Please add it to your .env file."
    )

# ----------------------------------------
# Connect to MongoDB via Docker
# ----------------------------------------
try:
    client = MongoClient(MONGO_URI)
    db = client["veinpay_db"]     
    users_collection = db["users"]
    print("[MongoDB via Docker] Connected successfully!")

except ConnectionFailure as e:
    print("[MongoDB via Docker] Connection failed:", e)
    raise e


def save_user_embedding(user_id: str, embedding):
    users_collection.update_one(
        {"user_id": user_id},
        {"$set": {"embedding": embedding}},
        upsert=True
    )
    print(f"[MongoDB] Embedding stored for user: {user_id}")

def get_user_embedding(user_id: str):
    user = users_collection.find_one({"user_id": user_id})
    if user:
        return user.get("embedding")
    return None
