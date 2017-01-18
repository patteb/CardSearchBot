#!/usr/bin/env python
# coding=utf-8

import time
import serial
import sys

from os import remove
from glob import glob

import matching
import cardbot_serial

# defaultvalues
max_pages = 1
query = "Urza's Hot Tub"
# total arbitzryry number, switch with expected value
likely_match = 700

# parsing inputparameters
if len(sys.argv) < 2:
    print "Please specify a query. Exiting."
    quit()
else:
    query = sys.argv[1]
    if len(sys.argv) > 2:
        max_pages = sys.argv[2]

# resolving the query
print("Querying the first " + str(max_pages) + " page(s) of \"" + query + "\" on Magiccards.info...")
query_imgs = matching.card_query(query, max_pages)
if query_imgs == 0:
    print("Search for \"" + query + "\" returned no results. Exiting.")
    quit()
print("Extracting features of query...")
kp_qry, des_qry = matching.query_features(query_imgs)
print("Deleting images...")
for file in glob(query + "*"):
    remove(file)

# initialize serial connection to arduino
serIF = cardbot_serial.init()

# Enter container-mode
while True:
    # Feed the first card
    print("Feeding next card...")
    cardbot_serial.feed(serIF)

    # Resolving the recorded image !!SIMULATED!!! drop "_dummy" 4 da real shit
    print("Finding features of card...")
    kp_cam, des_cam = matching.cam_features_dummy("cam.jpg")

    print("Matching...")
    matches = matching.card_matching(des_qry, des_cam)
    print("Max. score is " + str(matches))

    print("Sorting...")
    cardbot_serial.sort(matches > likely_match, serIF)


