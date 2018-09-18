#!/usr/bin/env python
# coding=utf-8


import cardbot_serial
import matching
import setup
from scryfall import scryfall

query, config, ser_if = setup.init()

img_files = scryfall(config.url_pre, query)  # API-call, download images
cv_img = matching.card_query(img_files)  # imread() downloaded images

# extracting features of all found cards ("ref" as in reference)
print("Extracting features of references...")
kp_ref, des_ref = matching.ref_features(cv_img)

setup.remove_temp(config.path)  # cleanup, delete card images

matches_found = 0
# Enter container-mode
while True:
    # Feed the first card
    print("Feeding next card."),
    if cardbot_serial.feed(ser_if):
        # Resolving the recorded image !!SIMULATED!!! drop "_dummy" 4 da real shit
        print("Finding features of card."),
        kp_cam, des_cam = matching.cam_features_dummy("cam.jpg", config.cam_if)

        print("Matching."),
        img_match = matching.card_matching(des_ref, des_cam)
        print("Max. score is " + str(img_match) + "."),
    else:
        print "\nFeeding Error! Exiting."
        quit()

    print("Sorting...")
    if cardbot_serial.sort(img_match > config.likely_match, ser_if):
        if (img_match > config.likely_match) and (config.max_matches is not None):
            matches_found += 1
            if (matches_found >= config.max_matches):
                print ("Maximum matching cards found. " + str(matches_found) + " matching cards found. Exiting.")
                quit()
        continue
    else:
        print "Sorting Error! Exiting"
        quit()
