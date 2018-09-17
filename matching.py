# coding=utf-8

import cv2


def ref_features(query_img):
    """Extracting features of a list of images
    ---------------------------
    IN: List of already imread() images
    OUT: List of Keypoints and descriptors of those images"""

    orb = cv2.ORB_create()
    kp_org = list()
    des_org = list()
    i = 1
    # for every card in the input list, extract Keypoints and descriptors and list them.
    for src in query_img:
        kp, des = orb.detectAndCompute(src, None)
        kp_org.append(kp)
        des_org.append(des)
        print("\r\tImage " + str(i) + "/" + str(len(query_img))),  # trailing comma to omit newline
        i += 1
    print "done!"
    return kp_org, des_org


def cam_features_dummy(cam_img, cam_if):
    """Dummy cam_features function, for testing purposes
    ---------------------------
    SEE cam_features"""
    orb = cv2.ORB_create()
    cam = cv2.imread(cam_img)
    kp_cam, des_cam = orb.detectAndCompute(cam, None)
    return kp_cam, des_cam


def cam_features(cam_if):
    """Taking an Image from the cam and find its Keypoints and Descriptors
    ---------------------------
    IN: Camera interface (from config-file)
    OUT: Keypoints and Descriptors of taken image"""
    # Create camera and feature detection object
    cam = cv2.VideoCapture(cam_if)
    orb = cv2.ORB()
    # take image
    s, img = cam.read()
    # extract keypoints and descriptors if successful
    if s:
        kp_cam, des_cam = orb.detectAndCompute(img, None)
        return kp_cam, des_cam
    else:
        return -1


def card_query(qry):
    """" Search for cards and imread() their images
    both input parameters are only passed to a subfunction.
    ---------------------------
    IN: list of downloaded images
    OUT: List of imread() card images."""
    if qry != 0:
        results = list()
        for src in qry:
            results.append(cv2.imread(src))
        return results
    else:
        return 0


def card_matching(des_qry, des_cam):
    """Feature match webcam-image against features of every card in query
    ---------------------------
    IN: Descriptors of query and camera
    OUT: maximum feature match score"""
    score = 0
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    for des in des_qry:
        tmp_score = len(bf.match(des_cam, des))
        if tmp_score > score:
            score = tmp_score
    return score
