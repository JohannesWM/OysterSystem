import data
import time


def temp():
    # get data
    return 28


def ph():
    # get data
    return 7.1


def salinity():
    # get data
    return 1234


while True:
    data.log(temp(), ph(), salinity())
    time.sleep(600)
