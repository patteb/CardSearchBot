# coding=utf-8

import configure
import os
from sys import argv
from glob import glob

import cardbot_serial


def init():
    # load config
    config = configure.configuration("config")
    config.read()

    # parsing input parameters
    if len(argv) < 2:
        print "Please specify a query. Exiting."
        quit()
    else:
        query = argv[1]
        if len(argv) > 2:
            max_pages = int(argv[2])
        else:
            max_pages = int(config.max_pages)

    # make temp-directory for image files, if not existent
    if not os.path.exists("temp"):
        os.makedirs("temp")

    # initialize serial connection to arduino
    serIF = cardbot_serial.init(config)

    return query, max_pages, config, serIF

def remove_temp():
    print("Deleting images...")
    for file in glob("temp/*.jpg"):
        os.remove(file)
