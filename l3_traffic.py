#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
from time import sleep
import RPi.GPIO as GPIO


class G(object):
    """docstring for G"""

    isRequest = False

    def __init__(self):
        super(G, self).__init__()
        # self.arg = arg

    @staticmethod
    def config():
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

    # input signal, startstop bottom and reset bottom
        GPIO.setup(G.abutton, GPIO.IN)
        GPIO.setup(G.bbutton, GPIO.IN)

    # 4 data LEDs, output signal
        GPIO.setup(G.portsA[0], GPIO.OUT)
        GPIO.setup(G.portsA[1], GPIO.OUT)
        GPIO.setup(G.portsA[2], GPIO.OUT)
        GPIO.setup(G.portsB[0], GPIO.OUT)
        GPIO.setup(G.portsB[1], GPIO.OUT)
        GPIO.setup(G.portsB[2], GPIO.OUT)

    @staticmethod
    def tick(a, b):
        sleep(1)
        a.ctime = a.ctime + 1
        b.ctime = b.ctime + 1

   # TODO modify these parameters to suit the hardware 
    abutton = 22
    bbutton = 17
    portsA = (10,9,11)
    portsB = (2,3,4)

    @staticmethod
    def getARequest():
        # just for test, get a interrupt
        value = GPIO.input(G.abutton)
        #value = raw_input("intrupt A?")
        print "button a value is {0}".format(value)
        if value:
            print "***** A is requested *****"
        return G.__chargeValue(value)

    @staticmethod
    def getBRequest():
        # just for test, get a interrupt
        value = GPIO.input(G.bbutton)
        #value = raw_input("intrupt B?")
        print "button b value is {0}".format(value)
        if value:
            print "***** B is requested *****"
        return G.__chargeValue(value)

    @staticmethod
    def changALight(arr):
        # input A ports here
        aports = G.portsA 
        print "changALight {1}, arr is {0}".format(arr, aports)
        GPIO.output(aports[0], arr[0])
        GPIO.output(aports[1], arr[1])
        GPIO.output(aports[2], arr[2])

    @staticmethod
    def changBLight(arr):
        # input B ports here
        aports = G.portsB 
        print "changBLight {1}, arr is {0}".format(arr, aports)
        GPIO.output(aports[0], arr[0])
        GPIO.output(aports[1], arr[1])
        GPIO.output(aports[2], arr[2])

    @staticmethod
    def __chargeValue(value):
        if value:
            if G.isRequest:
                print "stop requested!"
                return False
            else:
                return True
        return False


class Traffic(object):
    """docstring for Traffic"""
    redtime = 8
    greentime = 5
    yellowtime = 3

    def __init__(self, _id, lname, clr):
        super(Traffic, self).__init__()
        # color 0:red, 1:yellow, 2:green
        self._id = _id
        self.lname = lname
        self.cclor = clr
        self.ctime = 1
        self.sleepCnt = 0
        self.__changeLight()

    def checkStatus(self):
        if self.cclor == 0 and self.ctime > Traffic.redtime:
            # red to green
            self.__changeToColor(2)
            # if change on light to green, isRequset to False
            G.isRequest = False
        elif self.cclor == 1 and self.ctime > Traffic.yellowtime:
            # yellow to red
            self.__changeToColor(0)
        elif self.cclor == 2 and self.ctime > Traffic.greentime:
            # green to yellow
            self.__changeToColor(1)
        # self.__changeLight()

    def getStatus(self, input=None):
        if input is None:
            return "red" if self.cclor == 0 else "green" if self.cclor == 2 else "yellow"
        else:
            return "red" if input == 0 else "green" if input == 2 else "yellow"

    def __changeToColor(self, color):
        print "{0} change color from {1} to {2}".format(self.lname, self.getStatus(), self.getStatus(color))
        self.ctime = 1
        self.cclor = color
        self.__changeLight()

    def __changeLight(self):
        if self.cclor == 0:
            # print "change to red"
            if self._id == 0:
                G.changALight((1, 0, 0))
            else:
                G.changBLight((1, 0, 0))
        elif self.cclor == 1:
            # print "change to yellow"
            if self._id == 0:
                G.changALight((0, 1, 0))
            else:
                G.changBLight((0, 1, 0))
        elif self.cclor == 2:
            # print "change to green"
            if self._id == 0:
                G.changALight((0, 0, 1))
            else:
                G.changBLight((0, 0, 1))

    def processReq(self, other):
        # can do request only the color is red
        if self.cclor == 0 and self.ctime < 6:
            print "change current light ctime to 6, other light to yellow"
            self.ctime = 6
            other.__changeToColor(1)
            # other.ctime = 2
            G.isRequest = True
        else:
            print "{0}'s request is not responsed, check color and ctime".format(self.lname)


if __name__ == '__main__':
    G.config()
    # a is red
    a = Traffic(0, "Light A", 0)
    # b is green
    b = Traffic(1, "Light B", 2)
    while True:
        # clock tick
        print "{2} current time is {0}, color is {1}".format(a.ctime, a.getStatus(), a.lname)
        print "{2} current time is {0}, color is {1}".format(b.ctime, b.getStatus(), b.lname)
        print "G.isRequest = {0}".format(G.isRequest)
        G.tick(a, b)

        # response request
        if G.getARequest():
            a.processReq(b)
        elif G.getBRequest():
            b.processReq(a)

        # check status
        a.checkStatus()
        b.checkStatus()

        print "\n"
