import cv2
import numpy as np

def preprocess_image(image: np.ndarray) -> np.ndarray:
    """
    Takes a decoded RGB/BGR image and converts to a cleaned grayscale image.
    Steps:
    - BGR → Gray
    - Resize to 224×224
    - Histogram equalization
    """

    if image is None:
        raise ValueError("Input image is None in preprocess_image")

    # Convert BGR → Gray
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Resize for consistency
    resized = cv2.resize(gray, (224, 224))

    # Histogram equalization
    eq = cv2.equalizeHist(resized)

    return eq
