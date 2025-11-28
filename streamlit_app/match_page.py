import streamlit as st
import requests
from config import BACKEND_URL


def show_match_page():
    st.markdown("<div class='page-title'>Match Verification</div>", unsafe_allow_html=True)
    st.markdown(
        "<div class='sub-text'>Upload or capture an image to verify identity using vein biometrics.</div>",
        unsafe_allow_html=True
    )

    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)

    # -----------------------------
    # USER ID INPUT
    # -----------------------------
    st.markdown("<div class='section-label'>Enter User ID</div>", unsafe_allow_html=True)
    user_id = st.text_input("User ID", placeholder="example: anand").strip()

    # -----------------------------
    # FILE UPLOAD
    # -----------------------------
    st.markdown("<br><div class='section-label'>Upload Image</div>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader(
        "Upload an image for matching",
        type=["jpg", "jpeg", "png"],
        accept_multiple_files=False
    )

    # -----------------------------
    # CAMERA INPUT
    # -----------------------------
    st.markdown("<div class='section-label'>Or Capture Using Camera</div>", unsafe_allow_html=True)
    camera_img = st.camera_input("Capture from camera")

    # Priority: Camera first, then upload
    final_image_file = camera_img if camera_img else uploaded_file

    st.markdown("<br>", unsafe_allow_html=True)

    # -----------------------------
    # MATCH BUTTON
    # -----------------------------
    if st.button("Match Now"):

        if not user_id:
            st.error("Please enter a User ID.")
            return

        if final_image_file is None:
            st.error("Please upload or capture an image.")
            return

        with st.spinner("Matching... please wait."):

            # Convert image → bytes
            img_bytes = final_image_file.getvalue()

            files = {
                "file": ("image.jpg", img_bytes, "image/jpeg")
            }

            try:
                response = requests.post(
                    f"{BACKEND_URL}/match",
                    params={"user_id": user_id},    # correct for backend
                    files=files
                )

                if response.status_code == 200:
                    result = response.json()

                    similarity = float(result.get("similarity", 0.0))
                    match_status = bool(result.get("match", False))

                    # -------------------------
                    # MATCH SUCCESS
                    # -------------------------
                    if match_status:
                        st.success(f"Match Successful")
                        st.markdown(
                            f"""
                            <div class="glass-card" style="border-left: 4px solid #10b981; padding: 15px;">
                                <h4 style='color:#10b981;'>MATCH FOUND</h4>
                                <p>Similarity Score: <b>{round(similarity, 4)}</b></p>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )

                    # -------------------------
                    # MATCH FAILED
                    # -------------------------
                    else:
                        st.error("No Match Found")
                        st.markdown(
                            f"""
                            <div class="glass-card" style="border-left: 4px solid #ef4444; padding: 15px;">
                                <h4 style='color:#ef4444;'>MATCH FAILED</h4>
                                <p>Similarity Score: <b>{round(similarity, 4)}</b></p>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )

                else:
                    st.error(f"Error {response.status_code}")
                    try:
                        st.json(response.json())
                    except:
                        st.write(response.text)

            except Exception as e:
                st.error(f"Request failed: {e}")

    st.markdown("</div>", unsafe_allow_html=True)
