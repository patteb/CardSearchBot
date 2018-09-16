# coding=utf-8
from time import sleep

import serial


#  1-char codes for communication
# -----------------------------------
# sym - dir - translation
# -----------------------------------
# f - out - feed new card
# q - out - query state of container
# m - out - match
# c - out - no match ("chaff")
# n - in - negative confirmation
# y - in - positive confirmation

def init(config):
    """ Initialising Serial Connection to config-object specifics
        ---------------
        IN: configuration-object
        OUT: Serial interface object"""
    ser_if = serial.Serial(config.serial_if, config.baud, timeout=config.timeout)
    sleep(1.6)  # wait for serial port to be ready TODO: find a way to check
    return ser_if


def query_feed(ser_if):
    """ Query the arduino to check if the card container ist empty
        ---------------
        IN: Serial interface object
        OUT: Boolean TRUE if empty, FALSE if non-empty"""
    ser_if.write('q')
    return check_response(ser_if)


def feed(ser_if):
    """ Query the arduino to feed next card to camera
        ---------------
        IN: Serial interface object
        OUT: Boolean TRUE if done, FALSE on error"""
    while query_feed(ser_if):  # true if empty
        feed_continue = raw_input("Card reservoir is empty, continue? [Y/n] > ") or "Y"
        if (feed_continue == "n") or (feed_continue == "N"):
            print("Goodbye then. Exiting.")
            quit()
    ser_if.write('f')
    return check_response(ser_if)


def sort(match, ser_if):
    """ Query the arduino to sort the scanned card
        ---------------
        IN: (Boolean match) is card a match, Serial interface object
        OUT: Boolean TRUE if done, FALSE on error"""
    if match:
        ser_if.write('m')
    else:
        ser_if.write('c')
    return check_response(ser_if)


def check_response(ser_if):  # TODO:timeout handling
    """ Query the arduino to feed next card to camera
        ---------------
        IN: Serial interface object
        OUT: Boolean TRUE on positive response, FALSE on negative response"""
    if str(ser_if.read()) == 'y':
        return True
    else:
        return False
