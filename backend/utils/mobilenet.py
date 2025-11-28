import numpy as np
import tensorflow as tf
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input

# Load MobileNetV2 once at startup
base_model = MobileNetV2(
    weights="imagenet",
    include_top=False,
    pooling="avg",
    input_shape=(224, 224, 3)
)

def get_embedding(gray_img: np.ndarray) -> np.ndarray:
    """
    Convert extracted vein grayscale image → 3-channel → MobileNet embedding.
    """

    # Expand grayscale → RGB
    img_rgb = np.stack([gray_img, gray_img, gray_img], axis=-1)

    img_rgb = img_rgb.astype(np.float32)
    img_rgb = np.expand_dims(img_rgb, axis=0)

    img_rgb = preprocess_input(img_rgb)

    embedding = base_model.predict(img_rgb, verbose=0)
    embedding = embedding.flatten()

    return embedding
