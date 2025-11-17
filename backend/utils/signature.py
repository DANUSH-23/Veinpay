import cv2
import hashlib
import numpy as np
from numpy.linalg import norm

# ---------------------------------------------
# Signature Generation
# ---------------------------------------------
def generate_signature(skeleton_img):
    """
    Input: 255-based skeleton image
    Output: SHA256 hash (string)
    """

    # Resize for consistency
    resized = cv2.resize(skeleton_img, (128, 128))  
    flat = resized.flatten().tobytes()

    # Return hash as unique biometric signature
    signature = hashlib.sha256(flat).hexdigest()
    return signature


# ---------------------------------------------
# Signature Comparison (Exact or Hash Similarity)
# ---------------------------------------------
def compare_signatures(sig1, sig2):
    """
    Compares two SHA256 signatures.
    If they match exactly → 100% identical skeleton pattern.
    """
    return sig1 == sig2
