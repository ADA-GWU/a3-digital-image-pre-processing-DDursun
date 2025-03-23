import os
import random
import cv2
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # Needed for 3D projections

def crimmins_short(img, passes=3, threshold=2):
    """
    A simple, iterative Crimmins filter using np.roll.
    - 'passes': how many times to repeat the procedure
    - 'threshold': difference at which we increment/decrement
    
    Note: This version wraps around edges because of np.roll.
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
        # Clip to valid range after each pass
        out = np.clip(out, 0, 255)
    return out.astype(np.uint8)

# Path to your speckle folder
folder_path = "images/speckle"

# List all files in the folder (any extension)
all_files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]

if len(all_files) < 3:
    print("Not enough images in the folder.")
else:
    # Pick 3 random files
    selected_files = random.sample(all_files, 3)

    for fname in selected_files:
        img_path = os.path.join(folder_path, fname)
        # Read the image in grayscale
        img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
        if img is None:
            print(f"Error loading {fname}")
            continue

        # --- Column 2: Crimmins with multiple passes (stronger effect) ---
        crimmins_filtered = crimmins_short(img, passes=5, threshold=1)

        # --- Column 3: Combined Gaussian–Mean Pipeline ---
        # 1) Median filter (3×3)
        step1 = cv2.medianBlur(img, 3)
        # 2) Gaussian filter (3×3)
        step2 = cv2.GaussianBlur(step1, (3, 3), 0)
        # 3) Mean (Box) filter (3×3)
        step3 = cv2.blur(step2, (3, 3))
        # 4) Final median filter (5×5)
        combined = cv2.medianBlur(step3, 5)

        # Create a 2×3 figure:
        # Row 1 -> 2D images (Original, Crimmins, Combined)
        # Row 2 -> 3D surfaces with downsampling
        fig = plt.figure(figsize=(18, 12))

        # ------------------ Row 1: 2D images ------------------
        ax1 = fig.add_subplot(2, 3, 1)
        ax1.imshow(img, cmap='gray')
        ax1.set_title(f"{fname} - Original")
        ax1.axis("off")

        ax2 = fig.add_subplot(2, 3, 2)
        ax2.imshow(crimmins_filtered, cmap='gray')
        ax2.set_title("Crimmins (3 passes)")
        ax2.axis("off")

        ax3 = fig.add_subplot(2, 3, 3)
        ax3.imshow(combined, cmap='gray')
        ax3.set_title("Gaussian–Mean Pipeline")
        ax3.axis("off")

        # ------------------ Row 2: 3D surfaces (downsampled) ------------------
        # Build meshgrid
        X, Y = np.meshgrid(np.arange(img.shape[1]), np.arange(img.shape[0]))

        # Choose a stride for downsampling
        stride = 5  # plot every 5th pixel

        # Convert to float for plotting
        Z_orig = img.astype(float)
        Z_crim = crimmins_filtered.astype(float)
        Z_comb = combined.astype(float)

        # 4) Original 3D
        ax4 = fig.add_subplot(2, 3, 4, projection='3d')
        ax4.plot_surface(X[::stride, ::stride],
                         Y[::stride, ::stride],
                         Z_orig[::stride, ::stride],
                         cmap='gray', rstride=1, cstride=1)
        ax4.set_title("Original (3D)")

        # 5) Crimmins 3D
        ax5 = fig.add_subplot(2, 3, 5, projection='3d')
        ax5.plot_surface(X[::stride, ::stride],
                         Y[::stride, ::stride],
                         Z_crim[::stride, ::stride],
                         cmap='gray', rstride=1, cstride=1)
        ax5.set_title("Crimmins (3D)")

        # 6) Combined 3D
        ax6 = fig.add_subplot(2, 3, 6, projection='3d')
        ax6.plot_surface(X[::stride, ::stride],
                         Y[::stride, ::stride],
                         Z_comb[::stride, ::stride],
                         cmap='gray', rstride=1, cstride=1)
        ax6.set_title("Gaussian–Mean (3D)")

        plt.tight_layout()
        plt.show()
