#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import datetime
from time import sleep
import RPi.GPIO as GPIO
from Adafruit_7Segment import SevenSegment
# ===========================================================================
# Clock Example
# ===========================================================================
segment = SevenSegment(address=0x70)
counter = 0
minute = 0

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# input signal, startstop bottom and reset bottom
GPIO.setup(24, GPIO.IN)
GPIO.setup(23, GPIO.IN)
flg = True
while(True):
    reset = GPIO.input(24)
    startstop = GPIO.input(23)
    if reset:
        counter = 0
        minute = 0

    if startstop and flg:
        flg = False
    if startstop and not flg:
        flg = True

    if not flg:
        sleep(1)
        print "stopped"
    else:
        a4 = counter % 10
        a3 = counter / 10
        a2 = minute % 10
        a1 = minute / 10
        segment.writeDigit(4, a4)
        segment.writeDigit(3, a3)
        # segment.writeDigit(1,a2)
        # segment.writeDigit(0,a1)
        segment.setColon(counter % 2)
        segment.writeDigit(1, a2)
        segment.writeDigit(0, a1)
        sleep(1)

        counter = counter + 1
        if counter == 60:
            counter = 0
            minute = minute + 1
    # now = datetime.datetime.now()
    # hour = now.hour
    # minute = now.minute
    # second = now.second
    # # Set hours
    # segment.writeDigit(0, int(hour / 10)) # Tens
    # segment.writeDigit(1, hour % 10) # Ones
    # # Set minutes
    # segment.writeDigit(3, int(minute / 10)) # Tens
    # segment.writeDigit(4, minute % 10) # Ones
    # # Toggle color
    # segment.setColon(second % 2) # Toggle colon at 1Hz
    # # Wait one second
    # time.sleep(1)
