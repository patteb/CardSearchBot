# coding=utf-8

import argparse
import os
from glob import glob

import configparser

import cardbot_serial


# from sys import argv


class configuration(object):
    url_pre = "https://api.scryfall.com/cards/search?unique=art&q="
    path = "temp"
    likely_match = 700
    cam_if = 0
    serial_if = '/dev/ttymxc0'
    baud = 115200
    timeout = 3
    max_matches = None

    def __init__(self, file):
        self.file = file

    def read(self):
        config_parse = configparser.ConfigParser()
        config_parse.read(self.file)
        self.url_pre = config_parse['Query']['url_pre']
        self.path = config_parse['Query']['path']
        self.likely_match = config_parse['Matching']['likely_match']
        self.cam_if = config_parse['Matching']['cam_interface']
        self.serial_if = config_parse['Serial']['serial_interface']
        self.baud = config_parse['Serial']['baud']
        self.timeout = int(config_parse['Serial']['timeout'])
        self.max_matches = None


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
    if args.matches is not None:
        config.max_matches = int(args.matches)

    # make temp-directory for image files, if not existent
    if not os.path.exists(config.path):
        os.makedirs(config.path)

    # initialize serial connection to arduino
    ser_if = cardbot_serial.init(config)

    return query, config, ser_if


def remove_temp(path):
    """Removing downloaded jpg"""
    print("Deleting images...")
    for i in glob(path + "/*.jpg"):
        os.remove(i)


def init_parse():
    """ Initialising command-line parser, adding command line options"""
    parser = argparse.ArgumentParser(description='CardSearchBot. Search your cards.')
    parser.add_argument('-s', '--search', default="Dream Stalker", help="Name of the card to search for")
    # parser.add_argument('-s', '--search', default="Urza's Hot Tub", help="Name of the card to search for",
    # required=True)
    parser.add_argument('-c', '--config', default='config', help="Path to configuration file")
    parser.add_argument('-m', '--matches', help="Stop after n matches")

    return parser
