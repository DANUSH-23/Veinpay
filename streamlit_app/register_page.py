import streamlit as st
import requests
from PIL import Image
import io
from config import BACKEND_URL

def show_register_page():

    st.markdown("<div class='page-title'>User Registration</div>", unsafe_allow_html=True)
    st.markdown(
        "<div class='sub-text'>Upload 3–5 vein images for stronger, more accurate biometric registration.</div>", 
        unsafe_allow_html=True
    )

    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)

    st.markdown("<div class='section-label'>Enter User ID</div>", unsafe_allow_html=True)
    user_id = st.text_input("User ID", placeholder="Enter unique user ID")

    st.markdown("<br><div class='section-label'>Upload 3–5 Images</div>", unsafe_allow_html=True)

    uploaded_files = st.file_uploader(
        "Upload multiple sample images",
        type=["jpg", "jpeg", "png"],
        accept_multiple_files=True
    )

    st.markdown("<div class='section-label'>Optional: Capture using Camera</div>", unsafe_allow_html=True)

    camera_img = st.camera_input("Capture from camera")

    if camera_img:
        # Convert camera image to UploadedFile-like object
        uploaded_files.append(camera_img)

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("Register User"):
        if not user_id:
            st.error("Please enter a User ID.")
            return

        if not uploaded_files or len(uploaded_files) < 3:
            st.error("Please upload at least 3 images for robust registration.")
            return

        # 3–5 enforced
        if len(uploaded_files) > 5:
            st.warning("Only first 5 images will be used.")
            uploaded_files = uploaded_files[:5]

        with st.spinner("Processing and registering user..."):
            files = []
            for img in uploaded_files:
                img_bytes = img.read()
                files.append(
                    ("files", (img.name, img_bytes, img.type))
                )

            response = requests.post(
                f"{BACKEND_URL}/register",
                data={"user_id": user_id},
                files=files
            )

            if response.status_code == 200:
                res = response.json()
                st.success(f"User '{user_id}' registered successfully!")
                st.json(res)
            else:
                st.error("Registration failed.")
                try:
                    st.json(response.json())
                except:
                    st.write("No valid JSON returned.")

    st.markdown("</div>", unsafe_allow_html=True)
