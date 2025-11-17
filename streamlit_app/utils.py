import requests
from config import BACKEND_URL

def register_user(user_id, image_bytes):
    url = f"{BACKEND_URL}/register?user_id={user_id}"
    files = {"file": ("image.jpg", image_bytes, "image/jpeg")}
    return requests.post(url, files=files)

def match_user(user_id, image_bytes):
    url = f"{BACKEND_URL}/match?user_id={user_id}"
    files = {"file": ("image.jpg", image_bytes, "image/jpeg")}
    return requests.post(url, files=files)
