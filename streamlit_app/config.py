# streamlit_app/config.py

import os
from dotenv import load_dotenv

# Load variables from .env (located in project root)
load_dotenv()


# Backend FastAPI URL
BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")

# MongoDB URI for analytics
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
