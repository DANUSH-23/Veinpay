from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
import cv2

from backend.utils.preprocess import preprocess_image
from backend.utils.extract_vein import extract_vein_pattern
from backend.utils.signature import generate_signature, compare_signatures
from backend.db.database import save_user_signature, get_user_signature


app = FastAPI()

# -----------------------------
# CORS for React Frontend
# -----------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# Health Check
# -----------------------------
@app.get("/ping")
async def ping():
    return {"status": "Backend is running"}


# -----------------------------
# REGISTER USER (Step 1)
# -----------------------------
@app.post("/register")
async def register(user_id: str, file: UploadFile = File(...)):
    """
    Receives palm/hand image → preprocess → extract vein → generate signature → save to DB
    """

    # Load image bytes
    contents = await file.read()
    nparr = np.frombuffer(contents, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    if img is None:
        return {"error": "Invalid image uploaded"}

    # Preprocess
    pre_img = preprocess_image(img)

    # Extract vein pattern
    skeleton, gabor_img, thresh_img = extract_vein_pattern(pre_img)

    # Generate signature
    signature = generate_signature(skeleton)

    # Save to DB
    save_user_signature(user_id, signature)

    return {
        "status": "Registration Successful",
        "user_id": user_id,
        "signature_generated": True
    }


# -----------------------------
# MATCH USER (Step 2)
# -----------------------------
@app.post("/match")
async def match(user_id: str, file: UploadFile = File(...)):
    """
    Receives new palm scan → extract signature → compare with stored signature
    """

    # Load uploaded image
    contents = await file.read()
    nparr = np.frombuffer(contents, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    if img is None:
        return {"error": "Invalid image uploaded"}

    # Preprocess
    pre_img = preprocess_image(img)

    # Extract vein pattern
    skeleton, gabor_img, thresh_img = extract_vein_pattern(pre_img)

    # Generate signature from new scan
    new_signature = generate_signature(skeleton)

    # Get stored signature
    stored_signature = get_user_signature(user_id)

    if not stored_signature:
        return {"match": False, "error": "User not found"}

    # Compare
    match_result = compare_signatures(new_signature, stored_signature)

    return {
        "user_id": user_id,
        "match": match_result
    }
