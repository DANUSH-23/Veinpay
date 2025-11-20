from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
import cv2
from typing import List

from backend.utils.preprocess import preprocess_image
from backend.utils.extract_vein import extract_vein_pattern
from backend.utils.mobilenet import get_embedding
from backend.db.database import save_user_embedding, get_user_embedding

from sklearn.metrics.pairwise import cosine_similarity


app = FastAPI(
    title="VeinPay Authentication API",
    description="Backend for Vein-Based Biometric Authentication",
    version="2.0"
)

# -------------------------------------------------
# CORS
# -------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------------------------------
# Root
# -------------------------------------------------
@app.get("/")
def root():
    return {"status": "VeinPay backend running successfully"}


# -------------------------------------------------
# Multi-Sample Registration Endpoint
# -------------------------------------------------
@app.post("/register")
async def register(user_id: str, files: List[UploadFile] = File(...)):
    try:
        user_id = user_id.strip()
        if len(files) < 1:
            raise HTTPException(status_code=400, detail="Upload at least one image")

        embeddings = []

        for file in files:
            image_bytes = await file.read()
            np_img = np.frombuffer(image_bytes, np.uint8)
            img = cv2.imdecode(np_img, cv2.IMREAD_COLOR)

            if img is None:
                raise HTTPException(status_code=400, detail="Invalid image uploaded")

            # 1. Preprocess
            pre_img = preprocess_image(img)
            skeleton, gabor_img, thresh_img = extract_vein_pattern(pre_img)

            # 2. Generate embedding
            emb = get_embedding(gabor_img)
            embeddings.append(emb)

        # Average embedding from 3–5 samples
        final_embedding = np.mean(embeddings, axis=0).tolist()

        # Save to MongoDB
        save_user_embedding(user_id, final_embedding)

        return {
            "success": True,
            "message": f"User '{user_id}' registered with {len(files)} samples.",
            "samples_used": len(files)
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# -------------------------------------------------
# Match Endpoint (Single Image)
# -------------------------------------------------
@app.post("/match")
async def match(user_id: str, file: UploadFile = File(...)):
    try:
        user_id = user_id.strip()

        image_bytes = await file.read()
        np_img = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(np_img, cv2.IMREAD_COLOR)

        if img is None:
            raise HTTPException(status_code=400, detail="Invalid image file")

        # 1. Extract features
        pre_img = preprocess_image(img)
        skeleton, gabor_img, thresh_img = extract_vein_pattern(pre_img)

        # 2. Convert to embedding
        embedding = get_embedding(gabor_img)

        # 3. Retrieve stored embedding
        stored_emb = get_user_embedding(user_id)
        if stored_emb is None:
            raise HTTPException(status_code=404, detail="User not found")

        stored_emb = np.array(stored_emb, dtype=np.float32)

        # 4. Compute similarity
        similarity = float(cosine_similarity([embedding], [stored_emb])[0][0])

        # 5. Thresholding
        match_result = similarity >= 0.75

        return {
            "success": True,
            "match": bool(match_result),
            "similarity": similarity
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
