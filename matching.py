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
            gray = cv2.imread(src, 0)
            gray_rot = imutils.rotate_bound(gray, -90)
            blur = cv2.GaussianBlur(gray_rot, (5, 5), 0)
            blur_canny = cv2.Canny(blur, 50, 200)
            retval.append(imutils.resize(blur_canny, width=int(blur_canny.shape[1] * .5)))
        return retval
    else:
        return 0


def resize_match(reference, cam):
    """
    Match template by resizing cam-image. This is done to find best match if references and cam-image are not same size.
    :param reference: list of prepared images ( see ref_prepare)
    :param cam: prepared image from camera
    :return: matching score
    """
    (tH, tW) = reference.shape[:2]
    found = None

    for scale in np.linspace(0.2, 1.0, 20)[::-1]:
        resized = imutils.resize(cam, width=int(cam.shape[1] * scale))
        r = cam.shape[1] / float(resized.shape[1])
        if resized.shape[0] < tH or resized.shape[1] < tW:
            break

        # detect edges in the resized, grayscale image and apply template
        # matching to find the template in the image
        edged = cv2.Canny(resized, 50, 200)
        result = cv2.matchTemplate(edged, reference, cv2.TM_CCOEFF)
        (_, maxVal, _, maxLoc) = cv2.minMaxLoc(result)

        # if we have found a new maximum correlation value, then update
        # the bookkeeping variable
        if found is None or maxVal > found[0]:
            found = (maxVal, maxLoc, r)

    return int(maxVal / 1000000)


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
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # grey colorscale
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        retval = cv2.Canny(blur, 50, 200)
        return retval
    else:
        return -1


def card_matching(ref, cam):
    """Template match webcam-image against every card in query
    :param ref: list of prepared reference-images
    :param cam: prepared camera-image
    :return: Maximum score
    """
    score = 0
    for ref_image in ref:
        tmp_score = resize_match(ref_image, cam)
        if tmp_score > score:
            score = tmp_score
    return score
