import streamlit as st
from utils import match_user
from PIL import Image
import io

st.title("🧬 Match User")
st.markdown('<div class="card">', unsafe_allow_html=True)

user_id = st.text_input("Enter User ID")

st.write("### Upload Palm Image or Capture via Webcam")
uploaded_file = st.file_uploader("Upload File", type=["jpg", "jpeg", "png"])
camera_input = st.camera_input("Take Picture")

image_to_use = None

if uploaded_file:
    image_to_use = Image.open(uploaded_file)
elif camera_input:
    image_to_use = Image.open(camera_input)

if image_to_use:
    st.image(image_to_use, caption="Preview", use_container_width=True)

if st.button("Match"):
    if not image_to_use or not user_id:
        st.error("Please provide user ID and image.")
    else:
        img_bytes = io.BytesIO()
        image_to_use.save(img_bytes, format="JPEG")

        response = match_user(user_id, img_bytes.getvalue())

        if response.status_code == 200:
            res = response.json()
            st.success(f"Match Result: {res['match']}")
            st.metric("Similarity Score", f"{res['score']:.4f}")
            st.json(res)
        else:
            st.error("Match failed.")
            st.json(response.json())

st.markdown("</div>", unsafe_allow_html=True)
