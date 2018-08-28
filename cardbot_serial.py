# coding=utf-8
import serial


# 1-char codes for communication
# -----------------------------------
# sym - dir - translation
# -----------------------------------
# f - out - feed new card
# q - out - query state of container
# m - out - match
# c - out - no match ("chaff")
# n - in - negative confirmation
# y - in - positive confirmation

def query_feed(serIF):
    # mockup: TODO: serial communication, polling if container is empty
    serIF.write('q')
    # "Is the container empty?"
    if serIF.read() == 'n':
        return False
    else:
        return True


def feed(serIF):
    while (query_feed(serIF)):  # true if empty
        feed_continue = ""
        try:
            feed_continue = raw_input("Card reservoir is empty, continue? [Y/n] > ")
        except SyntaxError:
            feed_continue = "Y"
        if (feed_continue == "n") or (feed_continue == "N"):
            print("Goodbye then. Exiting.")
            quit()
    serIF.write('f')
    return


def init(config):
    return serial.Serial(config.serial_if, config.baudrate, config.timeout)


def sort(match, ser_if):
    if match:
        ser_if.write('m')
    else:
        ser_if.write('c')
    if ser_if.read() == 'y':
        return
