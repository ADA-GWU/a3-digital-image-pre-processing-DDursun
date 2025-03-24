import os
import random
import matplotlib.pyplot as plt
import cv2
import numpy as np

# Random image selection
random_nums = random.sample(range(1, 13), 2)

# Read images as grayscale
img1 = cv2.imread(os.path.join("images", "chemical", f"inchi{random_nums[0]}.png"), cv2.IMREAD_GRAYSCALE)
img2 = cv2.imread(os.path.join("images", "chemical", f"inchi{random_nums[1]}.png"), cv2.IMREAD_GRAYSCALE)

if img1 is None or img2 is None:
    print("Error loading images")
else:
    def process_image(image):
        
        inverted = cv2.bitwise_not(image)

        #1: Closing Only (Dilation + Erosion)
        kernel = np.ones((2, 2), np.uint8) 
        dilated = cv2.dilate(inverted, kernel, iterations=1)  
        closed = cv2.erode(dilated, kernel, iterations=1) 
        closed_final = cv2.bitwise_not(closed)

        #2: Connected Component Analysis Only
        num_labels, labels, stats, _ = cv2.connectedComponentsWithStats(inverted, connectivity=8)
        min_area = 2  
        cleaned = np.zeros_like(inverted)
        for i in range(1, num_labels):  
            if stats[i, cv2.CC_STAT_AREA] >= min_area:
                cleaned[labels == i] = 255
        cleaned_final = cv2.bitwise_not(cleaned)  

        #3: Both
        
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

    closed1, cleaned1, both1 = process_image(img1)
    closed2, cleaned2, both2 = process_image(img2)

    # Plotting image 1
    fig1, axes1 = plt.subplots(1, 4, figsize=(20, 5))
    axes1[0].imshow(img1, cmap='gray')
    axes1[0].set_title(f"inchi{random_nums[0]}.png - Original")
    axes1[0].axis("off")

    axes1[1].imshow(closed1, cmap='gray')
    axes1[1].set_title("Closing Only")
    axes1[1].axis("off")

    axes1[2].imshow(cleaned1, cmap='gray')
    axes1[2].set_title("Connected Component Only")
    axes1[2].axis("off")

    axes1[3].imshow(both1, cmap='gray')
    axes1[3].set_title("Closing + Connected Component")
    axes1[3].axis("off")

    plt.tight_layout()
    plt.show()

    # Plotting image 2
    fig2, axes2 = plt.subplots(1, 4, figsize=(20, 5))
    axes2[0].imshow(img2, cmap='gray')
    axes2[0].set_title(f"inchi{random_nums[1]}.png - Original")
    axes2[0].axis("off")

    axes2[1].imshow(closed2, cmap='gray')
    axes2[1].set_title("Closing Only")
    axes2[1].axis("off")

    axes2[2].imshow(cleaned2, cmap='gray')
    axes2[2].set_title("Connected Component Only")
    axes2[2].axis("off")

    axes2[3].imshow(both2, cmap='gray')
    axes2[3].set_title("Closing + Connected Component")
    axes2[3].axis("off")

    plt.tight_layout()
    plt.show()