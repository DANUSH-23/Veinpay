import numpy as np


def compute_skeleton_signature(skeleton_img: np.ndarray) -> float:
    """
    Simple scalar signature from a skeleton image.

    Currently:
        fraction of non-zero (white) pixels.

    Used only for analytics or debugging (not core matching).
    """
    if skeleton_img is None:
        return 0.0

    total = float(skeleton_img.size)
    if total == 0:
        return 0.0

    non_zero = float(np.count_nonzero(skeleton_img))
    return non_zero / total
