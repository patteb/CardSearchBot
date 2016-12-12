#!/usr/bin/env python
# coding=utf-8

import time

from os import remove
from glob import glob
import sys

import matching

# Defaultvalues
max_pages = 1
query = "Urza's Hot Tub"

# Verarbeitung der Kommandozeilenparameter
if len(sys.argv) < 2:
    print "Please specify a query. Exiting."
    quit()
else:
    query = sys.argv[1]
    if len(sys.argv) > 2:
        max_pages = sys.argv[2]

# Verarbetung der query
print("Querying the first "+str(max_pages)+" page(s) of \"" + query + "\" on Magiccards.info...")
query_imgs = matching.card_query(query, max_pages)
if query_imgs == 0:
    print("Search for \"" + query + "\" returned no results. Exiting.")
    quit()
print("Extracting features of query...")
kp_qry, des_qry = matching.query_features(query_imgs)
print("Deleting images...")
for file in glob(query + "*"):
    remove(file)

tic = time.time()
# Verarbeitung des kamerabildes !!SIMULIERT!!! drop "_dummy" 4 da real shit
print("Finding features of card...")
kp_cam, des_cam = matching.cam_features_dummy("cam.jpg")

print("Matching...")
matches = matching.card_matching(des_qry, des_cam)
toc = time.time()

print(str(toc - tic))
print("Max. score is " + str(matches))
