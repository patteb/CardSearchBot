import cv2

import cardcrawler

def query_features(query_img):
    orb = cv2.ORB()
    kp_org = list()
    des_org =list()
    for src in query_img:
        kp, des = orb.detectAndCompute(src, None)
        kp_org.append(kp)
        des_org.append(des)
    return(kp_org,des_org)

def cam_features_dummy(cam_img):
    orb = cv2.ORB()
    cam = cv2.imread(cam_img)
    kp_cam, des_cam = orb.detectAndCompute(cam, None)
    return(kp_cam,des_cam)

def cam_features(cam_img):
    cam = VideoCapture(0)
    orb = cv2.ORB()
    s, img = cam.read()
    #imwrite("cam.jpg", img)
    #cam = cv2.imread(cam_img)
    if s:
        kp_cam, des_cam = orb.detectAndCompute(img, None)
    return(kp_cam,des_cam)

def card_query(query,max_pages):
    qry = cardcrawler.crawler(query, max_pages)
    if qry != 0:
        results = list()
        for src in qry:
            results.append(cv2.imread(src))
        return results
    else:
        return 0


def card_matching(des_qry,des_cam):
    score = 0
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    for des in des_qry:
        tmp_score = len(bf.match(des_cam,des))
        if tmp_score > score:
            score = tmp_score
    return(score)
