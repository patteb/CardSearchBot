#!/usr/bin/env python
# coding=utf-8


import cardbot_serial
import matching
import scryfall
import setup

query, config, ser_if = setup.init()

url = scryfall.build_query(config.url_pre, query)  # construct query url
img_url = scryfall.api_query(url)  # API-Call

img_files = scryfall.card_download(img_url)  # download images
cv_img = matching.card_query(url)  # imread() downloaded images

# extracting features of all found cards ("ref" as in reference)
print("Extracting features of query...")
kp_ref, des_ref = matching.ref_features(cv_img)

setup.remove_temp()  # cleanup, delete card images

# Enter container-mode
while True:
    # Feed the first card
    print("Feeding next card. "),
    if cardbot_serial.feed(ser_if):
        # Resolving the recorded image !!SIMULATED!!! drop "_dummy" 4 da real shit
        print("Finding features of card. "),
        kp_cam, des_cam = matching.cam_features_dummy("cam.jpg", config.cam_if)

        print("Matching. "),
        matches = matching.card_matching(des_ref, des_cam)
        print("Max. score is " + str(matches)),
    else:
        print "\nFeeding Error! Exiting."
        quit()

    print(" Sorting...")
    if cardbot_serial.sort(matches > config.likely_match, ser_if):
        continue
    else:
        print "Sorting Error! Exiting"
        quit()
