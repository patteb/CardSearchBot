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
# y - in - positive confimation

def query_feed(serIF):
    # mockup: TODO: serial communication, polling if container is empty
    serIF.write('q')
    # "Is the container empty?"
    if serIF.read() == 'n':
        return (False)
    else:
        return (True)


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


def init(IF,bd,to):
    return (serial.Serial(IF, bd, to))


def sort(match, serIF):
    if match:
        serIF.write('m')
    else:
        serIF.write('c')
    if serIF.read() == 'y':
        return
