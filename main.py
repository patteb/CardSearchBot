#!/usr/bin/env python
# coding=utf-8

import hardware
import image_processing as imp
import setup
from scryfall import scryfall

query, config, ser_if = setup.init()
hw = hardware.hardware(config) # initalize hardware

img_files = scryfall(config.url_pre, query)  # API-call, download images
cv_img = imp.ref_list(img_files)  # prepare downloaded images

setup.remove_temp(config.path)  # cleanup, delete card images

matches_found = 0
# Enter container-mode
while True:
    # Feed the first card
    print("Feeding next card."),
    if hw.feed():
        # Resolving the recorded image !!SIMULATED!!! drop "_dummy" 4 da real shit
        # sleep(.2)
        print("Taking Picture, extracting card."),
        cam_img = imp.take_picture(config.cam_if, cv_img)
        print("Matching."),
        img_match = imp.matching(cv_img, cam_img)
        print("Score is %.f%%." % img_match),
        if img_match > config.likely_match:
            matches_found += 1
            print ("Match #%s found!" % matches_found),
    else:
        print "\nFeeding Error! Exiting."
        quit()

    print("Sorting...")
    if hw.sort(img_match > config.likely_match, ser_if):
        if (img_match > config.likely_match) and (config.max_matches is not None):
            if matches_found >= config.max_matches:
                print ("Maximum matching cards found. %s matching cards found. Exiting." % matches_found)
                quit()
        continue
    else:
        print "Sorting Error! Exiting"
        quit()
