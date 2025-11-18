import streamlit as st
import requests
from PIL import Image
import io
from config import load_env

config = load_env()
BACKEND_URL = config["BACKEND_URL"]


def show_register_page():
    st.markdown("<div class='page-title'>Register User</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-text'>Enroll a new palm-vein signature.</div>", unsafe_allow_html=True)

    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)

    col1, col2 = st.columns([1.3, 1])

    with col1:
        user_id = st.text_input("User ID")

        mode = st.radio("Choose Method", ["Upload Image", "Use Camera"])

        img = None
        if mode == "Upload Image":
            uploaded_file = st.file_uploader("Upload palm image", type=["jpg", "jpeg", "png"])
            if uploaded_file:
                img = Image.open(uploaded_file)
        else:
            camera = st.camera_input("Capture Image")
            if camera:
                img = Image.open(camera)

        if img:
            st.session_state["reg_preview"] = img

        if st.button("Register"):
            if not user_id:
                st.error("User ID required.")
                return
            if img is None:
                st.error("Image required.")
                return

            buffer = io.BytesIO()
            img.save(buffer, format="JPEG")
            buffer.seek(0)

            files = {"file": ("upload.jpg", buffer, "image/jpeg")}

            with st.spinner("Processing & extracting vein embedding..."):
                resp = requests.post(
                    f"{BACKEND_URL}/register",
                    params={"user_id": user_id},
                    files=files,
                    timeout=90
                )

                if resp.status_code == 200:
                    st.success("User Registered Successfully!")
                    st.json(resp.json())
                else:
                    st.error("Registration failed.")
                    st.code(resp.text)

    with col2:
        st.markdown("<p class='section-label'>Preview</p>", unsafe_allow_html=True)
        if "reg_preview" in st.session_state:
            st.image(st.session_state["reg_preview"], use_container_width=True)
        else:
            st.markdown("<p class='placeholder-text'>No image selected.</p>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)
