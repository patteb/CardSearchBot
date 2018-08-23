# coding=utf-8

import configparser


class configuration(object):
    mci1 = "https://api.scryfall.com/cards/search?unique=art&q="

    likely_match = 700
    cam_if = 0
    serial_if = '/dev/ttymxc0'
    baudrate = 9600
    timeout = 1

    def __init__(self, file):
        self.file = file

    def read(self):
        configparse = configparser.ConfigParser()
        configparse.read(self.file)
        self.mci1 = configparse['Query']['mci_query1']
        self.likely_match = configparse['Matching']['likely_match']
        self.cam_if = configparse['Matching']['cam_interface']
        self.serial_if = configparse['Serial']['serial_interface']
        self.baudrate = configparse['Serial']['baudrate']
        self.timeout = configparse['Serial']['timeout']
