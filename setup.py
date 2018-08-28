# coding=utf-8

import os
from glob import glob
from sys import argv

import cardbot_serial
import configure


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

    # make temp-directory for image files, if not existent
    if not os.path.exists("temp"):
        os.makedirs("temp")

    # initialize serial connection to arduino
    ser_if = cardbot_serial.init(config)

    return query, config, ser_if


def remove_temp():
    print("Deleting images...")
    for i in glob("temp/*.jpg"):
        os.remove(i)
