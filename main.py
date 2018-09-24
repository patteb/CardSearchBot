#!/usr/bin/env python
# coding=utf-8


from time import sleep

import cardbot_serial
import matching
import setup
from scryfall import scryfall

query, config, ser_if = setup.init()

img_files = scryfall(config.url_pre, query)  # API-call, download images
cv_img = matching.ref_prepare(img_files)  # prepare downloaded images
des_ref = matching.ref_features(cv_img)

setup.remove_temp(config.path)  # cleanup, delete card images

matches_found = 0
# Enter container-mode
while True:
    # Feed the first card
    print("Feeding next card."),
    if cardbot_serial.feed(ser_if):
        # Resolving the recorded image !!SIMULATED!!! drop "_dummy" 4 da real shit
        sleep(1)
        print("Taking Picture."),
        cam_img = matching.cam_prepare(config.cam_if)
        print("Extracting features."),
        des_cam = matching.cam_features(cam_img)
        print("Matching."),
        img_match = matching.card_matching(des_ref, des_cam)
        print("Score is %s." % img_match),
        if img_match > config.likely_match:
            matches_found += 1
            print ("Match #%s found!" % matches_found),
    else:
        print "\nFeeding Error! Exiting."
        quit()

    print("Sorting...")
    if cardbot_serial.sort(img_match > config.likely_match, ser_if):
        if (img_match > config.likely_match) and (config.max_matches is not None):
            if matches_found >= config.max_matches:
                print ("Maximum matching cards found. %s matching cards found. Exiting." % matches_found)
                quit()
        continue
        sleep(1)
    else:
        print "Sorting Error! Exiting"
        quit()
