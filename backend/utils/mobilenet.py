import numpy as np
import cv2

from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.preprocessing.image import img_to_array

# -------------------------------------------------
# Load MobileNetV2 once at import time
# -------------------------------------------------
base_model = MobileNetV2(
    weights="imagenet",
    include_top=False,
    pooling="avg",
    input_shape=(224, 224, 3),
)


def get_embedding(bgr_img: np.ndarray) -> np.ndarray:
    """
    Extracts a feature embedding from an image using MobileNetV2.

    Steps:
    - Ensure 3-channel image
    - Convert BGR → RGB
    - Resize to 224x224
    - Preprocess using keras.applications.mobilenet_v2.preprocess_input
    - Run through MobileNetV2 (global average pooled)
    - Flatten to 1D embedding

    Returns:
        np.ndarray of shape (embedding_dim,)
    """

    if bgr_img is None:
        raise ValueError("bgr_img is None in extract_embedding")

    # If grayscale, convert to 3-channel BGR
    if len(bgr_img.shape) == 2:
        bgr_img = cv2.cvtColor(bgr_img, cv2.COLOR_GRAY2BGR)

    # BGR → RGB
    rgb = cv2.cvtColor(bgr_img, cv2.COLOR_BGR2RGB)

    # Resize for MobileNetV2
    rgb = cv2.resize(rgb, (224, 224))

    # To tensor
    x = img_to_array(rgb)
    x = np.expand_dims(x, axis=0)

    # Preprocess as MobileNet expects
    x = preprocess_input(x)

    # Forward pass
    features = base_model.predict(x, verbose=0)

    # Flatten
    embedding = features.flatten()
    return embedding
