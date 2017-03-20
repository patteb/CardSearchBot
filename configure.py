# coding=utf-8

import configparser

class configuration(object):
    max_pages = 1
    mci1 = "http://magiccards.info/query?q=%2B%2B"
    mci2 = "&v=scan&s=cname&p="
    likely_match = 700
    cam_if = 0
    serial_if = '/dev/ttymxc0'
    baudrate = 9600
    timeout = 1

    def __init__(self,file):
        self.file=file

    def read(self):
        configparse = configparser.ConfigParser()
        configparse.read(self.file)
        self.max_pages = configparse['Query']['max_pages']
        self.mci1 = configparse['Query']['mci_query1']
        self.mci2 = configparse['Query']['mci_query2']
        self.likely_match = configparse['Matching']['likely_match']
        self.cam_if = configparse['Matching']['cam_interface']
        self.serial_if = configparse['Serial']['serial_interface']
        self.baudrate = configparse['Serial']['baudrate']
        self.timeout = configparse['Serial']['timeout']



