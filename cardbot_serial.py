# coding=utf-8
import serial


# TODO: function docstrings

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

def query_feed(ser_if):
    # mockup: TODO: serial communication, polling if container is empty
    ser_if.write('q')
    # "Is the container empty?"
    if ser_if.readline() == 'n':
        return False
    else:
        return True


def feed(ser_if):
    while query_feed(ser_if):  # true if empty
        try:
            feed_continue = raw_input("Card reservoir is empty, continue? [Y/n] > ")
        except SyntaxError:
            feed_continue = "Y"
        if (feed_continue == "n") or (feed_continue == "N"):
            print("Goodbye then. Exiting.")
            quit()
    ser_if.write('f')
    return


def init(config):
    ser_if = serial.Serial(config.serial_if, config.baud, timeout=None)  # config.timeout)
    return ser_if


def sort(match, ser_if):
    if match:
        ser_if.write('m')
    else:
        ser_if.write('c')
    if ser_if.read() == 'y':
        return
