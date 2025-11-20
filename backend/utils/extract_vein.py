import cv2
import numpy as np


def extract_vein_pattern(preprocessed_img: np.ndarray):
    """
    Takes a preprocessed grayscale image and:

    - Applies a Gabor filter to enhance vein-like structures.
    - Applies adaptive thresholding.
    - Extracts a morphological skeleton of the veins.

    Returns:
        skeleton, gabor_norm, thresh_img
    """

    if preprocessed_img is None:
        raise ValueError("Preprocessed image is None in extract_vein_pattern.")

    # Ensure grayscale
    if len(preprocessed_img.shape) == 3:
        preprocessed_img = cv2.cvtColor(preprocessed_img, cv2.COLOR_BGR2GRAY)

    # Ensure uint8
    if preprocessed_img.dtype != np.uint8:
        preprocessed_img = np.clip(preprocessed_img * 255, 0, 255).astype(np.uint8)

    # ---------------------------------------------
    # 1. Apply Gabor filter to emphasize veins
    # ---------------------------------------------
    g_kernel = cv2.getGaborKernel(
        (21, 21),  # kernel size
        8.0,       # sigma
        0.0,       # theta
        10.0,      # lambda
        0.5,       # gamma
        0.0,       # psi
        ktype=cv2.CV_32F,
    )

    gabor = cv2.filter2D(preprocessed_img, cv2.CV_8UC3, g_kernel)

    # Normalize Gabor output to [0, 255] uint8
    gabor_norm = cv2.normalize(gabor, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)

    # ---------------------------------------------
    # 2. Adaptive Thresholding (requires uint8 gray)
    # ---------------------------------------------
    thresh_img = cv2.adaptiveThreshold(
        gabor_norm,
        255,
        cv2.ADAPTIVE_THRESH_MEAN_C,
        cv2.THRESH_BINARY_INV,
        21,
        10,
    )

    # ---------------------------------------------
    # 3. Morphological Skeletonization
    # ---------------------------------------------
    size = np.size(thresh_img)
    skeleton = np.zeros(thresh_img.shape, np.uint8)
    element = cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3))
    temp = thresh_img.copy()
    done = False

    while not done:
        eroded = cv2.erode(temp, element)
        temp2 = cv2.dilate(eroded, element)
        temp2 = cv2.subtract(temp, temp2)
        skeleton = cv2.bitwise_or(skeleton, temp2)
        temp = eroded.copy()

        zeros = size - cv2.countNonZero(temp)
        if zeros == size:
            done = True

    return skeleton, gabor_norm, thresh_img
