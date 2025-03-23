import os
import random
import cv2
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def crimmins_short(img, passes=3, threshold=2):
    out = img.astype(np.int16)
    directions = [(-1,0), (1,0), (0,-1), (0,1), (-1,-1), (-1,1), (1,-1), (1,1)]
    for _ in range(passes):
        current = out.copy()
        for dr, dc in directions:
            shifted = np.roll(current, shift=(dr, dc), axis=(0,1))
            out = np.where(shifted >= (current + threshold), out + 1, out)
            out = np.where(shifted <= (current - threshold), out - 1, out)
        out = np.clip(out, 0, 255)
    return out.astype(np.uint8)

folder_path = "images/speckle"
all_files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
if len(all_files) < 3:
    print("Not enough images in the folder.")
else:
    selected_files = random.sample(all_files, 3)
    for fname in selected_files:
        img_path = os.path.join(folder_path, fname)
        img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
        if img is None:
            print(f"Error loading {fname}")
            continue

        crimmins_filtered = crimmins_short(img, passes=5, threshold=1)
        step1 = cv2.medianBlur(img, 3)
        step2 = cv2.GaussianBlur(step1, (3, 3), 0)
        step3 = cv2.blur(step2, (3, 3))
        combined = cv2.medianBlur(step3, 5)

        fig = plt.figure(figsize=(18, 12))
        # Row 1: 2D images
        ax1 = fig.add_subplot(2, 3, 1)
        ax1.imshow(img, cmap='gray')
        ax1.set_title(f"{fname} - Original", pad=10)
        ax1.axis("off")

        ax2 = fig.add_subplot(2, 3, 2)
        ax2.imshow(crimmins_filtered, cmap='gray')
        ax2.set_title("Crimmins (5 passes)", pad=10)
        ax2.axis("off")

        ax3 = fig.add_subplot(2, 3, 3)
        ax3.imshow(combined, cmap='gray')
        ax3.set_title("Gaussian–Mean Pipeline", pad=10)
        ax3.axis("off")

        # Row 2: 3D surfaces (downsampled)
        X, Y = np.meshgrid(np.arange(img.shape[1]), np.arange(img.shape[0]))
        stride = 5
        Z_orig = img.astype(float)
        Z_crim = crimmins_filtered.astype(float)
        Z_comb = combined.astype(float)

        ax4 = fig.add_subplot(2, 3, 4, projection='3d')
        ax4.plot_surface(X[::stride, ::stride], Y[::stride, ::stride],
                         Z_orig[::stride, ::stride], cmap='gray', rstride=1, cstride=1)
        

        ax5 = fig.add_subplot(2, 3, 5, projection='3d')
        ax5.plot_surface(X[::stride, ::stride], Y[::stride, ::stride],
                         Z_crim[::stride, ::stride], cmap='gray', rstride=1, cstride=1)
        

        ax6 = fig.add_subplot(2, 3, 6, projection='3d')
        ax6.plot_surface(X[::stride, ::stride], Y[::stride, ::stride],
                         Z_comb[::stride, ::stride], cmap='gray', rstride=1, cstride=1)
        

        plt.tight_layout()
        output_dir = "outputs/speckle_clean"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        save_path = os.path.join(output_dir, f"{os.path.splitext(fname)[0]}_clean.png")
        plt.savefig(save_path)
        plt.show()
