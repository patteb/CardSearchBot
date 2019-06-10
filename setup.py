# coding=utf-8

import argparse
import os
from glob import glob

import configparser

# from sys import argv

class configuration(object):
    url_pre = "https://api.scryfall.com/cards/search?unique=art&q="
    path = "temp"
    likely_match = .3
    cam_if = 0
    GPIO = 18
    ADC = 0x48
    thresh = 512
    Servo = 0x40
    servo_speed = 512
    sort_pin = 0
    feed_pin = 1
    max_matches = None

    def __init__(self, file):
        self.file = file

    def read(self):
        config_parse = configparser.ConfigParser()
        config_parse.read(self.file)
        self.url_pre = config_parse['Query']['url_pre']
        self.path = config_parse['Query']['path']
        self.likely_match = float(config_parse['Matching']['likely_match'])
        self.cam_if = int(config_parse['Matching']['cam_interface'])
        self.GPIO = int(config_parse['hardware']['GPIO'])
        self.ADC = hex(config_parse['hardware']['ADC'])
        self.thresh = int(config_parse['hardware']['thresh'])
        self.Servo = hex(config_parse['hardware']['Servo'])
        self.servo_speed = int(config_parse['hardware']['servo_speed'])
        self.sort_pin = int(config_parse['hardware']['sort_pin'])
        self.feed_pin = int(config_parse['hardware']['feed_pin'])
        self.max_matches = None


def init():
    """Initialising any pre-existing conditions, like sys-argv or config file
    ---------------
    :param:: void
    :return: the query to search for (as given via argv), a configuration-object and a serial-interface-object
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

    return query, config


def remove_temp(path):
    """Removing downloaded jpg"""
    print("Deleting images...")
    for i in glob(path + "/*.jpg"):
        os.remove(i)


def init_parse():
    """ Initialising command-line parser, adding command line options"""
    parser = argparse.ArgumentParser(description='CardSearchBot. Search your cards.')
    parser.add_argument('-s', '--search', default="Jhoira", help="Name of the card to search for")
    # parser.add_argument('-s', '--search', default="Urza's Hot Tub", help="Name of the card to search for",
    # required=True)
    parser.add_argument('-c', '--config', default='config', help="Path to configuration file")
    parser.add_argument('-m', '--matches', help="Stop after n matches")

    return parser
