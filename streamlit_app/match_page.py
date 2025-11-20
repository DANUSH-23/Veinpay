import streamlit as st
import requests
from PIL import Image
import numpy as np
import io
from config import BACKEND_URL

def show_match_page():
    st.markdown("<div class='page-title'>Match Verification</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-text'>Upload an image to verify identity using vein biometrics.</div>", unsafe_allow_html=True)

    with st.container():
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)

        user_id = st.text_input("Enter User ID", placeholder="example: anand").strip()

        uploaded_file = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png"])

        # CAMERA INPUT
        cam_img = st.camera_input("Or capture using camera")

        if cam_img:
            image_bytes = cam_img.getvalue()
        elif uploaded_file:
            image_bytes = uploaded_file.read()
        else:
            image_bytes = None

        if st.button("Match Now"):
            if not user_id:
                st.error("Please enter a User ID!")
            elif not image_bytes:
                st.error("Please upload or capture an image!")
            else:
                files = {
                    "file": ("image.jpg", image_bytes, "image/jpeg")
                }

                try:
                    response = requests.post(
                        f"{BACKEND_URL}/match",
                        params={"user_id": user_id},
                        files=files
                    )

                    if response.status_code == 200:
                        data = response.json()

                        similarity = round(data.get("similarity", 0.0), 4)
                        match = data.get("match", False)

                        if match:
                            st.success(f"✅ MATCH SUCCESSFUL — Similarity: {similarity}")
                        else:
                            st.error(f"❌ NO MATCH — Similarity: {similarity}")

                    else:
                        st.error(f"Error: {response.status_code} — {response.text}")

                except Exception as e:
                    st.error(f"Request failed: {e}")

        st.markdown("</div>", unsafe_allow_html=True)
