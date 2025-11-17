import cv2

def preprocess_image(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # CLAHE = Contrast Limited Adaptive Histogram Equalization
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    enhanced = clahe.apply(gray)

    # Noise reduction
    filtered = cv2.bilateralFilter(enhanced, 9, 75, 75)

    return filtered
