import cv2
import numpy as np

def preprocess_image(image_bytes):
    """
    Converts input image bytes into a clean preprocessed grayscale image.
    Steps:
    - Decode bytes
    - Convert BGR → Gray
    - Resize to fixed size
    - Apply histogram equalization
    """

    # Convert uploaded bytes to NumPy array
    nparr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    if img is None:
        raise ValueError("Invalid image data.")

    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Resize for consistency (MobileNetV2 expects fixed inputs)
    resized = cv2.resize(gray, (224, 224))

    # Enhance contrast
    eq = cv2.equalizeHist(resized)

    return eq
