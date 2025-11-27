from fastapi import FastAPI, UploadFile, File, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
import cv2
from sklearn.metrics.pairwise import cosine_similarity

from backend.utils.preprocess import preprocess_image
from backend.utils.extract_vein import extract_vein_pattern
from backend.utils.mobilenet import get_embedding
from backend.db.database import save_user_embedding, get_user_embedding


app = FastAPI(
    title="VeinPay Authentication API",
    version="1.0",
    description="Single-image vein registration and matching backend"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"message": "VeinPay backend running"}


# ----------------------------------------------------
# Register (SINGLE IMAGE)
# ----------------------------------------------------
@app.post("/register")
async def register(
    user_id: str = Query(..., description="Unique user ID"),
    file: UploadFile = File(...)
):

    try:
        # Read bytes
        image_bytes = await file.read()
        np_img = np.frombuffer(image_bytes, np.uint8)

        img = cv2.imdecode(np_img, cv2.IMREAD_COLOR)
        if img is None:
            raise HTTPException(400, "Could not decode image")

        # Preprocess
        gray = preprocess_image(img)

        # Extract vein pattern
        _, gabor_out, _ = extract_vein_pattern(gray)

        # MobileNet embedding
        embedding = get_embedding(gabor_out).tolist()

        # Store in DB
        save_user_embedding(user_id, embedding)

        return {
            "success": True,
            "user_id": user_id,
            "embedding_length": len(embedding),
            "message": "User registered successfully"
        }

    except Exception as e:
        raise HTTPException(500, f"Registration failed: {str(e)}")


# ----------------------------------------------------
# Match Endpoint
# ----------------------------------------------------
@app.post("/match")
async def match(
    user_id: str = Query(...),
    file: UploadFile = File(...)
):

    try:
        stored = get_user_embedding(user_id)
        if stored is None:
            raise HTTPException(404, "User not found")

        # Process uploaded image
        image_bytes = await file.read()
        np_img = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(np_img, cv2.IMREAD_COLOR)

        if img is None:
            raise HTTPException(400, "Could not decode image")

        gray = preprocess_image(img)
        _, gabor_out, _ = extract_vein_pattern(gray)
        emb_new = get_embedding(gabor_out)

        stored = np.array(stored, dtype=np.float32)

        similarity = float(cosine_similarity([emb_new], [stored])[0][0])
        match_result = similarity >= 0.75

        return {
            "success": True,
            "match": bool(match_result),
            "similarity": similarity
        }

    except Exception as e:
        raise HTTPException(500, f"Matching failed: {str(e)}")
