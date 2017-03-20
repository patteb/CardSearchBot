#!/usr/bin/env python
# coding=utf-8

import time
import serial
import sys
import configparser

from os import remove
from glob import glob

import matching
import cardbot_serial

#load config
config = configparser.ConfigParser()
config.read("config")
max_pages = config['Query']['max_pages']
query = config['Query']['query']
mci1 = config['Query']['mci_query1']
mci2 = config['Query']['mci_query2']
likely_match = config['Matching']['likely_match']
cam_if = config['Matching']['cam_interface']
serial_if = config['Serial']['interface']
serial_baudrate = config['Serial']['baudrate']
serial_timeout = config['Serial']['timeout']

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
url = mci1 + query + mci2
query_imgs = matching.card_query(url, max_pages)
if query_imgs == 0:
    print("Search for \"" + query + "\" returned no results. Exiting.")
    quit()
print("Extracting features of query...")
kp_qry, des_qry = matching.query_features(query_imgs)
print("Deleting images...")
for file in glob(query + "*"):
    remove(file)

# initialize serial connection to arduino
serIF = cardbot_serial.init(serial_if,serial_baudrate,serial_timeout)

# Enter container-mode
while True:
    # Feed the first card
    print("Feeding next card...")
    cardbot_serial.feed(serIF)

    # Resolving the recorded image !!SIMULATED!!! drop "_dummy" 4 da real shit
    print("Finding features of card...")
    kp_cam, des_cam = matching.cam_features_dummy("cam.jpg", cam_if)

    print("Matching...")
    matches = matching.card_matching(des_qry, des_cam)
    print("Max. score is " + str(matches))

    print("Sorting...")
    cardbot_serial.sort(matches > likely_match, serIF)


