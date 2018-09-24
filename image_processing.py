import cv2
import numpy as np


def preprocess_image(image):
    """Returns a grayed, blurred, and adaptively thresholded camera image."""

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    retval, thresh = cv2.threshold(blur, 100, 255, cv2.THRESH_BINARY)
    return thresh


def find_card(pre_proc):
    img, contours, hierarchy = cv2.findContours(pre_proc, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    return contours


def extract_card(img, contour):
    mask = np.zeros_like(img)  # Create mask where white is what we want, black otherwise

    cv2.drawContours(mask, contour, 1, 255, -1)  # Draw filled contour in mask
    out = np.zeros_like(img)  # Extract out the object and place into output image
    out[mask == 255] = img[mask == 255]

    # Now crop
    (x, y) = np.where(mask == 255)
    (topx, topy) = (np.min(x), np.min(y))
    (bottomx, bottomy) = (np.max(x), np.max(y))
    crop = out[topx:bottomx + 1, topy:bottomy + 1]
    return crop
