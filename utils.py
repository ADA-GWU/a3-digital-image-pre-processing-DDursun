import cv2
import numpy as np

def apply_sharpening(image):
    """Apply sharpening filter to a 2D numpy image (grayscale)."""
    kernel = np.array([[0, -1, 0],
                       [-1, 5,-1],
                       [0, -1, 0]])
    return cv2.filter2D(image, -1, kernel)

def crimmins_short(img, passes=3, threshold=2):
    """
    simple, iterative Crimmins filter using np.roll
    - 'passes': how many times to repeat the procedure
    - 'threshold': difference at which we increment/decrement
    
    """
    out = img.astype(np.int16)
    directions = [(-1,0), (1,0), (0,-1), (0,1), (-1,-1), (-1,1), (1,-1), (1,1)]
    
    for _ in range(passes):
        current = out.copy()
        for dr, dc in directions:
            shifted = np.roll(current, shift=(dr, dc), axis=(0,1))
            # Increase pixel by 1 if neighbor >= pixel + threshold
            out = np.where(shifted >= (current + threshold), out + 1, out)
            # Decrease pixel by 1 if neighbor <= pixel - threshold
            out = np.where(shifted <= (current - threshold), out - 1, out)
        out = np.clip(out, 0, 255)
    return out.astype(np.uint8)

