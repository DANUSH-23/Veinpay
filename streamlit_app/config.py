import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

def load_env():
    return {
        "BACKEND_URL": os.getenv("BACKEND_URL", "http://127.0.0.1:8000"),
        "MONGO_URI": os.getenv("MONGO_URI", "mongodb://localhost:27017")
    }

# Direct access for imports
env = load_env()
BACKEND_URL = env["BACKEND_URL"]
MONGO_URI = env["MONGO_URI"]
