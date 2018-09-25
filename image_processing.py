import cv2
import imutils as iu
import numpy as np
from skimage.measure import compare_ssim


def preprocess_image(image):
    """
    Returns a grayed and edge-found image.
    :param image: raw image input
    :return:grayed and edge-found image
    """
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.bilateralFilter(gray, 11, 17, 17)
    edged = cv2.Canny(gray, 30, 200)
    return edged


def extract_card(img):
    """
    Original author: Adrian Rosebrock
    https://www.pyimagesearch.com/2014/05/05/building-pokedex-python-opencv-perspective-warping-step-5-6/

    Cropping the Card out from a cam image, then perspective transform it to "square it up"
    :param img:
    :return:
    """
    _, contours, _ = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]

    for c in contours[1:]:
        # approximate the contour
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)

        # if our approximated contour has four points, then
        # we can assume that we have found our screen
        if len(approx) == 4:
            screenCnt = approx
            break

    try:
        # now that we have our screen contour, we need to determine
        # the top-left, top-right, bottom-right, and bottom-left
        # points so that we can later warp the image -- we'll start
        # by reshaping our contour to be our finals and initializing
        # our output rectangle in top-left, top-right, bottom-right,
        # and bottom-left order
        pts = screenCnt.reshape(4, 2)
        rect = np.zeros((4, 2), dtype="float32")

        # the top-left point has the smallest sum whereas the
        # bottom-right has the largest sum
        s = pts.sum(axis=1)
        rect[0] = pts[np.argmin(s)]
        rect[2] = pts[np.argmax(s)]

        # compute the difference between the points -- the top-right
        # will have the minumum difference and the bottom-left will
        # have the maximum difference
        diff = np.diff(pts, axis=1)
        rect[1] = pts[np.argmin(diff)]
        rect[3] = pts[np.argmax(diff)]

        # multiply the rectangle by the original ratio
        # rect *= ratio

        # now that we have our rectangle of points, let's compute
        # the width of our new image
        (tl, tr, br, bl) = rect
        widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
        widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))

        # ...and now for the height of our new image
        heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
        heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))

        # take the maximum of the width and height values to reach
        # our final dimensions
        maxWidth = max(int(widthA), int(widthB))
        maxHeight = max(int(heightA), int(heightB))

        # construct our destination points which will be used to
        # map the screen to a top-down, "birds eye" view
        dst = np.array([
            [0, 0],
            [maxWidth - 1, 0],
            [maxWidth - 1, maxHeight - 1],
            [0, maxHeight - 1]], dtype="float32")

        # calculate the perspective transform matrix and warp
        # the perspective to grab the screen
        M = cv2.getPerspectiveTransform(rect, dst)
        crop = cv2.warpPerspective(img, M, (maxWidth, maxHeight))

    except UnboundLocalError:
        print "\nContour Error! Exiting."
        quit()

    return crop


def shrink(ref, img):
    """
    Shrinking the card-image down to the size of the ref-images. This is needed for matching later on. This needs the
    reference-images to be the all same size.
    This does not keep the aspect ratio!
    :param ref: list of our references. this could be a single image, list is given for ease of use
    :param img: image to resize.
    :return:
    """
    h = ref[0].shape[0] / float(img.shape[0])
    w = ref[0].shape[1] / float(img.shape[1])
    shrinked = cv2.resize(img, None, fx=w, fy=h, interpolation=cv2.INTER_CUBIC)
    return shrinked


def preprocess_ref(img):
    """
    Preprocess a image to be used as referenced. References must be rotated to match the orientation of the cards in the
    hardware. This way, only a few reference images need to be rotated and not every scanned card.
    :param img:
    :return:
    """
    ref = iu.rotate_bound(img, -90)
    ref = iu.resize(ref, width=int(ref.shape[0] * .5))
    ref = preprocess_image(ref)
    return ref


def ref_list(img_files_list):
    """
    Prepares a list of references, ready to match
    :param img_files_list: list of file paths of downloaded images
    :return: list of preprocessed reference images
    """
    if img_files_list != 0:
        retval = list()
        for src in img_files_list:
            ref = cv2.imread(src)
            ref = preprocess_ref(ref)
            ref_180 = iu.rotate_bound(ref, 180)
            retval.append(ref)
            retval.append(ref_180)
        return retval
    else:
        return 0


def take_picture(cam_if, ref_list):
    """
    Scan a card and prepare the imaage for matching
    :param cam_if: Camera interface
    :param ref_list: list of preprocessed images, needed fpr shrinking
    :return:
    """
    cam = cv2.VideoCapture(cam_if)
    s, img = cam.read()
    if s:
        pre = preprocess_image(img)
        extracted = extract_card(pre)
        shrinked = shrink(ref_list, extracted)
        return shrinked
    else:
        return -1


def matching(ref_list, cam_pic):
    """
    Match a scanned card and keep score. The matching is made via structural similarity
    :param ref_list: list of prepared references to check against
    :param cam_pic: prepared card scan
    :return: a %-score
    """
    score = 0.0
    for ref in ref_list:
        (temp_score, _) = compare_ssim(ref, cam_pic, full=True)
        temp_score = temp_score * 100
        if temp_score > score:
            score = temp_score
    return score
