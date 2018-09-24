import cv2
import imutils
import numpy as np


def ref_prepare(qry):  # TODO: 180deg Rotation
    """
    Search for cards and imread() their images, rotate them, find edges
    both input parameters are only passed to a subfunction.
    Replaces: card_query(qry)
    -------------------------------------------------------
    :param qry: list of downloaded images
    :return: list of prepared reference images
    """
    if qry != 0:
        retval = list()
        for src in qry:
            ref = cv2.imread(src)
            ref_rot = imutils.rotate_bound(ref, -90)
            ref_resize = imutils.resize(ref_rot, width=int(ref_rot.shape[0] * .41), height=int(ref_rot.shape[1] * .41))
            ref_pre = preprocess_image(ref_resize)
            retval.append(ref_pre)
        return retval
    else:
        return 0


def ref_features(query_img):
    """Extracting features of a list of images
    ---------------------------
    IN: List of already imread() images
    OUT: List of Keypoints and descriptors of those images"""

    orb = cv2.ORB_create()
    des_org = list()
    i = 1
    # for every card in the input list, extract Keypoints and descriptors and list them.
    for src in query_img:
        _, des = orb.detectAndCompute(src, None)
        des_org.append(des)
        print("\r\tImage " + str(i) + "/" + str(len(query_img))),  # trailing comma to omit newline
        i += 1
    print "done!"
    return des_org


def cam_prepare(cam_if):
    """Taking an Image from the cam and prepare for matching
    --------------------------------------
    :param cam_if: Camera interface, see config
    :return: prepared image
    """
    # Create camera and feature detection object
    cam = cv2.VideoCapture(cam_if)
    s, img = cam.read()
    if s:
        pre = preprocess_image(img)
        contours = find_card(pre)
        extracted = extract_card(pre, contours)
        return extracted
    else:
        return -1


def cam_features(cam_img):
    """Taking an Image from the cam and find its Keypoints and Descriptors
    ---------------------------
    IN: prepared camera image
    OUT: Descriptors of taken image"""
    orb = cv2.ORB_create()
    _, des_cam = orb.detectAndCompute(cam_img, None)
    return des_cam


def card_matching(des_qry, des_cam):
    """Template match webcam-image against every card in query
    :param ref: list of prepared reference-images
    :param cam: prepared camera-image
    :return: Maximum score
    """
    score = 0
    bf = cv2.BFMatcher(cv2.NORM_L1, crossCheck=False)
    for des in des_qry:
        # tmp_score = resize_match(ref_image, cam)
        tmp_score = len(bf.match(des_cam, des))
        if tmp_score > score:
            score = tmp_score
    return score


def preprocess_image(image):
    """Returns a grayed, blurred, and adaptively thresholded camera image."""

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    retval, thresh = cv2.threshold(blur, 60, 255, cv2.THRESH_BINARY)
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
