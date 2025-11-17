import cv2
import numpy as np
from skimage.morphology import skeletonize

def apply_gabor_filter(img):
    # Gabor filter for vein texture enhancement
    kernels = []
    ksize = 21  # kernel size
    sigma = 5.0
    lambd = 10.0
    gamma = 0.5

    # Apply filters for multiple orientations
    for theta in np.arange(0, np.pi, np.pi / 8):
        params = {
            'ksize': (ksize, ksize),
            'sigma': sigma,
            'theta': theta,
            'lambd': lambd,
            'gamma': gamma,
            'psi': 0,
            'ktype': cv2.CV_32F
        }
        kern = cv2.getGaborKernel(**params)
        kernels.append(kern)

    accum = np.zeros_like(img, dtype=np.float32)

    for kern in kernels:
        fimg = cv2.filter2D(img, cv2.CV_8UC3, kern)
        np.maximum(accum, fimg, accum)

    return accum


def extract_vein_pattern(img):
    """
    Input: preprocessed grayscale image
    Output: skeletonized vein pattern
    """

    # 1. Gabor enhancement
    gabor_img = apply_gabor_filter(img)

    # Normalize back to 0–255
    gabor_norm = cv2.normalize(gabor_img, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)

    # 2. Adaptive Thresholding
    thresh = cv2.adaptiveThreshold(
        gabor_norm,
        255,
        cv2.ADAPTIVE_THRESH_MEAN_C,
        cv2.THRESH_BINARY_INV,
        25,
        15
    )

    # 3. Skeletonization with skimage
    skeleton = skeletonize(thresh // 255)  # input must be 0/1

    skeleton = (skeleton * 255).astype(np.uint8)

    return skeleton, gabor_norm, thresh
