import streamlit as st
import requests
from config import BACKEND_URL


def show_register_page():

    st.markdown("<div class='page-title'>User Registration</div>", unsafe_allow_html=True)
    st.markdown(
        "<div class='sub-text'>Upload a single vein image or capture using camera for registration.</div>",
        unsafe_allow_html=True
    )

    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)

    # -----------------------------
    # USER ID INPUT
    # -----------------------------
    st.markdown("<div class='section-label'>Enter User ID</div>", unsafe_allow_html=True)
    user_id = st.text_input("User ID", placeholder="Enter unique user ID")

    # -----------------------------
    # FILE UPLOAD
    # -----------------------------
    st.markdown("<br><div class='section-label'>Upload Image</div>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader(
        "Upload a single vein image",
        type=["jpg", "jpeg", "png"],
        accept_multiple_files=False
    )

    # -----------------------------
    # CAMERA INPUT
    # -----------------------------
    st.markdown("<div class='section-label'>Or Capture Using Camera</div>", unsafe_allow_html=True)
    camera_img = st.camera_input("Capture from camera")

    # Final image priority → camera first
    final_image_file = camera_img if camera_img else uploaded_file

    st.markdown("<br>", unsafe_allow_html=True)

    # -----------------------------
    # REGISTER BUTTON ACTION
    # -----------------------------
    if st.button("Register User"):

        if not user_id.strip():
            st.error("Please enter a User ID.")
            return

        if final_image_file is None:
            st.error("Please upload or capture an image.")
            return

        with st.spinner("Processing and registering user..."):

            # Convert image to bytes
            img_bytes = final_image_file.getvalue()

            # Send to backend
            response = requests.post(
                f"{BACKEND_URL}/register",
                params={"user_id": user_id},   # <-- CORRECT for backend
                files={"file": ("image.jpg", img_bytes, "image/jpeg")}
            )

            if response.status_code == 200:
                st.success(f"User '{user_id}' registered successfully!")
                st.json(response.json())
            else:
                st.error("Registration failed.")
                try:
                    st.json(response.json())
                except:
                    st.write("No valid JSON returned from backend.")

    st.markdown("</div>", unsafe_allow_html=True)
