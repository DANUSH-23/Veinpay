import streamlit as st
from utils import register_user
from PIL import Image
import io

st.title("🔐 Register User")
st.markdown('<div class="card">', unsafe_allow_html=True)

user_id = st.text_input("Enter User ID")

st.write("### Upload Palm Image or Capture via Webcam")
uploaded_file = st.file_uploader("Upload File", type=["jpg", "jpeg", "png"])
camera_input = st.camera_input("Take Picture")

image_to_use = None

# Uploaded image
if uploaded_file:
    image_to_use = Image.open(uploaded_file)

# Webcam image
elif camera_input:
    image_to_use = Image.open(camera_input)

# Show preview
if image_to_use:
    st.image(image_to_use, caption="Preview", use_container_width=True)

# Register button
if st.button("Register"):
    if not image_to_use or not user_id:
        st.error("Enter user ID and upload/capture an image.")
    else:
        img_bytes = io.BytesIO()
        image_to_use.save(img_bytes, format="JPEG")

        response = register_user(user_id, img_bytes.getvalue())

        if response.status_code == 200:
            st.success("User Registered Successfully!")
            st.json(response.json())
        else:
            st.error("Registration failed.")
            st.json(response.json())

st.markdown("</div>", unsafe_allow_html=True)
