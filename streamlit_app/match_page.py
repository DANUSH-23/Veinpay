import streamlit as st
import requests
from PIL import Image
import io
from config import BACKEND_URL


def show_match_page():
    st.markdown("<div class='page-title'>🔍 Match Vein Pattern</div>", unsafe_allow_html=True)
    st.write("Upload your hand image OR capture a live image using the camera.")

    # --- Image inputs ---
    uploaded_file = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png"])
    camera_file = st.camera_input("Capture Image")

    # Always show User ID
    user_id = st.text_input("Enter User ID", placeholder="example: user123")

    # Decide which image to use
    image_bytes = None
    if uploaded_file is not None:
        image_bytes = uploaded_file.read()
        st.image(uploaded_file, caption="Uploaded Image", width=300)
    elif camera_file is not None:
        image_bytes = camera_file.getvalue()
        st.image(camera_file, caption="Captured Image", width=300)

    # Match button
    if st.button("🔍 Match Now", use_container_width=True):
        if not user_id:
            st.error("User ID is required.")
            return

        if image_bytes is None:
            st.error("Please upload or capture an image first.")
            return

        files = {"file": ("image.jpg", image_bytes, "image/jpeg")}
        url = f"{BACKEND_URL}/match"
        params = {"user_id": user_id}

        with st.spinner("Matching vein patterns..."):
            try:
                resp = requests.post(url, params=params, files=files)

                if resp.status_code != 200:
                    st.error(f"Match failed (status {resp.status_code})")
                    try:
                        st.json(resp.json())
                    except Exception:
                        st.write(resp.text)
                    return

                result = resp.json()

                st.subheader("🔎 Match Result")
                st.success(f"Match: {result.get('match')}")

                # ----- Similarity / score handling -----
                sim = result.get("similarity", None)
                if sim is None:
                    # many backends use "score" instead of "similarity"
                    sim = result.get("score", None)

                if sim is not None:
                    try:
                        sim_val = float(sim)
                        st.metric("Similarity Score", f"{sim_val:.4f}")
                    except Exception:
                        # fallback if it's already a formatted string
                        st.metric("Similarity Score", str(sim))
                else:
                    st.warning("Similarity score not returned by backend.")

                with st.expander("Raw response"):
                    st.json(result)

            except Exception as e:
                st.error(f"Error talking to backend: {e}")
