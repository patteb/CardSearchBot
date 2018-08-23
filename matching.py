# coding=utf-8

import cv2
import cardcrawler


# Extracting features of a list of images
# ---------------------------
# IN: List of already imread() images
# OUT: List of Keypoints and descriptors of those images
def query_features(query_img):
    orb = cv2.ORB_create()
    kp_org = list()
    des_org = list()
    # for every card in the input list, extract Keypoints and descriptors and list them.
    for src in query_img:
        kp, des = orb.detectAndCompute(src, None)
        kp_org.append(kp)
        des_org.append(des)
    return kp_org, des_org


# Dummy cam_features function, for testing purposes
# ---------------------------
# SEE cam_features
def cam_features_dummy(cam_img, cam_if):
    orb = cv2.ORB_create()
    cam = cv2.imread(cam_img)
    kp_cam, des_cam = orb.detectAndCompute(cam, None)
    return kp_cam, des_cam


# Taking an Image from the cam and find its Keypoints and Descriptors
# ---------------------------
# IN: Camera interface (from config-file)
# OUT: Keypoints and Descriptors of taken image
def cam_features(cam_if):
    # Create camera and feature detection object
    cam = cv2.VideoCapture(cam_if)
    orb = cv2.ORB()
    # take image
    s, img = cam.read()
    # extract Keypoints and descriptors if successful
    if s:
        kp_cam, des_cam = orb.detectAndCompute(img, None)
    return kp_cam, des_cam


# Search for cards and imread() their images
# both input parameters are only passed to a subfunction.
# ---------------------------
# IN: search query url, maximum number of pages to browse
# OUT: List of imread() card images.
def card_query(url, max_pages):
    qry = cardcrawler.crawler(url, max_pages)
    if qry != 0:
        results = list()
        for src in qry:
            results.append(cv2.imread(src))
        return results
    else:
        return 0


# Feature match webcam-image against features of every card in query
# ---------------------------
# IN: Descriptors of query and camera
# OUT: maximum feature match score
def card_matching(des_qry, des_cam):
    score = 0
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    for des in des_qry:
        tmp_score = len(bf.match(des_cam, des))
        if tmp_score > score:
            score = tmp_score
    return score
