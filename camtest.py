# coding: utf8
from cv2 import *

# initialize the camera
cam = VideoCapture(0)  # 0 -> index of camera
s, img = cam.read()
if s:  # frame captured without any errors
    imwrite("filename.jpg", img)  # save image
