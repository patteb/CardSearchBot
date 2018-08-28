#!/usr/bin/env python
# coding=utf-8


import cardbot_serial
import matching
import scryfall
import setup

query, config, serIF = setup.init()
url = scryfall.build_query(config.mci1, query)  # construct query url
img_url = scryfall.api_query(url)  # API-Call

img_files = scryfall.card_download(img_url)  # download images
query_imgs = matching.card_query(url)  # imread() downloaded images

# extracting features of all found cards
print("Extracting features of query...")
kp_qry, des_qry = matching.query_features(query_imgs)

setup.remove_temp()  # cleanup, delete card images

# Enter container-mode
while True:
    # Feed the first card
    print("Feeding next card...")
    cardbot_serial.feed(serIF)

    # Resolving the recorded image !!SIMULATED!!! drop "_dummy" 4 da real shit
    print("Finding features of card...")
    kp_cam, des_cam = matching.cam_features_dummy("cam.jpg", config.cam_if)

    print("Matching...")
    matches = matching.card_matching(des_qry, des_cam)
    print("Max. score is " + str(matches))

    print("Sorting...")
    cardbot_serial.sort(matches > config.likely_match, serIF)
