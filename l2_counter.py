#!/usr/bin/env python
# -*- coding: utf-8 -*-


import time
from time import sleep
import RPi.GPIO as GPIO

# setup GPIO function and GPIO pin


GPIO_IN_STARTSTOP = 17
GPIO_IN_RESET = 22
GPIO_OUT_STATUS = 4
GPIO_OUT_0 = 25
GPIO_OUT_1 = 24
GPIO_OUT_2 = 23
GPIO_OUT_3 = 18
counter = 0
cntFlg = False


def config():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    # status LED, output signal shows startstop status
    GPIO.setup(GPIO_OUT_STATUS, GPIO.OUT)

    # input signal, startstop bottom and reset bottom
    GPIO.setup(GPIO_IN_STARTSTOP, GPIO.IN)
    GPIO.setup(GPIO_IN_RESET, GPIO.IN)

    # 4 data LEDs, output signal
    GPIO.setup(GPIO_OUT_0, GPIO.OUT)
    GPIO.setup(GPIO_OUT_1, GPIO.OUT)
    GPIO.setup(GPIO_OUT_2, GPIO.OUT)
    GPIO.setup(GPIO_OUT_3, GPIO.OUT)


def doCount():
    global counter
    counter = counter + 1
    print "now counter is {0}".format(counter)
    if counter == 16:
        counter = 0
    sleep(1)


def doDisplay():
                # display count
    global counter
    d0 = counter & 8
    d1 = counter & 4
    d2 = counter & 2
    d3 = counter & 1
    GPIO.output(GPIO_OUT_0, d0)
    GPIO.output(GPIO_OUT_1, d1)
    GPIO.output(GPIO_OUT_2, d2)
    GPIO.output(GPIO_OUT_3, d3)


def counting():
    GPIO.output(GPIO_OUT_STATUS, 1)
    # print ' ***startCounting*** '
    # global cntFlg
    # cntFlg = True
    # while cntFlg:
    doCount()
    doDisplay()


def endCounting():
    GPIO.output(GPIO_OUT_STATUS, 0)
    global cntFlg
    cntFlg = False
    doDisplay()

if __name__ == '__main__':

    # doCount()
    config()
    startStop = 0
    reset = 1
    while True:
        startStop = GPIO.input(GPIO_IN_STARTSTOP)
        reset = GPIO.input(GPIO_IN_RESET)
        print "startstop is {0}".format(startStop)
        print "reset is {0}".format(reset)
        print "cntFlg is {0}".format(cntFlg)
        if not reset:
            print "********* reseting ********"
            endCounting()
            counter = 0
            sleep(2)
        if startStop and cntFlg:
            print "********** end counting ********"
            endCounting()
            sleep(2)
        elif startStop and not cntFlg:
            print "********** start counting *********"
            cntFlg = True
            sleep(2)
        elif cntFlg:
            counting()
        else:
            print "now counter is {0}".format(counter)
            sleep(2)
        print "\n"

