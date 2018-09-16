# coding=utf-8

import argparse
import os
from glob import glob

import configparser

import cardbot_serial


# from sys import argv


class configuration(object):
    url_pre = "https://api.scryfall.com/cards/search?unique=art&q="

    likely_match = 700
    cam_if = 0
    serial_if = '/dev/ttymxc0'
    baud = 115200
    timeout = 3

    def __init__(self, file):
        self.file = file

    def read(self):
        config_parse = configparser.ConfigParser()
        config_parse.read(self.file)
        self.url_pre = config_parse['Query']['url_pre']
        self.likely_match = config_parse['Matching']['likely_match']
        self.cam_if = config_parse['Matching']['cam_interface']
        self.serial_if = config_parse['Serial']['serial_interface']
        self.baud = config_parse['Serial']['baud']
        self.timeout = int(config_parse['Serial']['timeout'])


def init():
    """Initialising any pre-existing conditions, like sys-argv or config file
    ---------------
    IN: void
    OUT: the query to search for (as given via argv), a configuration-object and a serial-interface-object
    """

    # parsing input parameters
    parser = init_parse()
    args = parser.parse_args()

    # load config
    config = configuration(args.config)
    config.read()

    query = args.search

    # if len(argv) < 2:
    #     print "Please specify a query. Exiting."
    #     query = "Urza's Hot Tub"
    #     quit()
    # else:
    #     query = argv[1]

    # make temp-directory for image files, if not existent
    if not os.path.exists("temp"):
        os.makedirs("temp")

    # initialize serial connection to arduino
    ser_if = cardbot_serial.init(config)

    return query, config, ser_if


def remove_temp():
    """Removing downloaded jpg"""
    print("Deleting images...")
    for i in glob("temp/*.jpg"):
        os.remove(i)


def init_parse():
    parser = argparse.ArgumentParser(description='CardSearchBot. Search your cards.')
    parser.add_argument('-s', '--search', default="Urza's Hot Tub", help="Name of the card to search for",
                        required=True)
    parser.add_argument('-c', '--config', default='config', help="Path to configuration file")
    return parser
