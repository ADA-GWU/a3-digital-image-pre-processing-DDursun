import os
import random
import matplotlib.pyplot as plt
import cv2
import numpy as np

# Random image selection
random_nums = random.sample(range(1, 13), 3)

def process_image(image):
    inverted = cv2.bitwise_not(image)

    # Closing Only (Dilation + Erosion)
    kernel = np.ones((2, 2), np.uint8) 
    dilated = cv2.dilate(inverted, kernel, iterations=1)  
    closed = cv2.erode(dilated, kernel, iterations=1) 
    closed_final = cv2.bitwise_not(closed)

    # Connected Component Analysis Only
    num_labels, labels, stats, _ = cv2.connectedComponentsWithStats(inverted, connectivity=8)
    min_area = 2  
    cleaned = np.zeros_like(inverted)
    for i in range(1, num_labels):  
        if stats[i, cv2.CC_STAT_AREA] >= min_area:
            cleaned[labels == i] = 255
    cleaned_final = cv2.bitwise_not(cleaned)  

    #3 Both
    kernel = np.ones((2, 2), np.uint8)
    dilated_both = cv2.dilate(inverted, kernel, iterations=1)
    closed_both = cv2.erode(dilated_both, kernel, iterations=1)
    num_labels_both, labels_both, stats_both, _ = cv2.connectedComponentsWithStats(closed_both, connectivity=8)
    cleaned_both = np.zeros_like(closed_both)
    for i in range(1, num_labels_both):  
        if stats_both[i, cv2.CC_STAT_AREA] >= min_area:
            cleaned_both[labels_both == i] = 255
    both_final = cv2.bitwise_not(cleaned_both)  

    return closed_final, cleaned_final, both_final

os.makedirs("outputs/noise_clean", exist_ok=True)

for idx in range(3):
    img_path = os.path.join("images", "chemical", f"inchi{random_nums[idx]}.png")
    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        print("Error loading image")
        continue

    closed, cleaned, both = process_image(img)

    fig, axes = plt.subplots(2, 4, figsize=(20, 8))

    axes[0, 0].imshow(img, cmap='gray')
    axes[0, 0].set_title(f"inchi{random_nums[idx]}.png - Original")
    axes[0, 0].axis("off")

    axes[0, 1].imshow(closed, cmap='gray')
    axes[0, 1].set_title("Closing Only")
    axes[0, 1].axis("off")

    axes[0, 2].imshow(cleaned, cmap='gray')
    axes[0, 2].set_title("Connected Component Only")
    axes[0, 2].axis("off")

    axes[0, 3].imshow(both, cmap='gray')
    axes[0, 3].set_title("Closing + Connected Component")
    axes[0, 3].axis("off")

    axes[1, 0].imshow(np.zeros_like(img), cmap='gray')
    axes[1, 0].set_title("")

    axes[1, 1].imshow(cv2.absdiff(img, closed), cmap='gray')
    axes[1, 1].set_title("Removed (Closing)")
    axes[1, 1].axis("off")

    axes[1, 2].imshow(cv2.absdiff(img, cleaned), cmap='gray')
    axes[1, 2].set_title("Removed (Component)")
    axes[1, 2].axis("off")

    axes[1, 3].imshow(cv2.absdiff(img, both), cmap='gray')
    axes[1, 3].set_title("Removed (Both)")
    axes[1, 3].axis("off")

    plt.tight_layout()
    save_path = os.path.join("outputs/noise_clean", f"inchi{random_nums[idx]}.png")
    fig.savefig(save_path, dpi=150)
    plt.show()
    plt.close(fig)
