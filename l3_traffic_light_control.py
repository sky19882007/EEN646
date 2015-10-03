#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
from time import sleep
# import RPi.GPIO as GPIO


class GpioCtrl(object):
    """docstring for GpioCtrl"""
    n = 0
    interruptFlag = 0

    def __init__(self):
        super(GpioCtrl, self).__init__()

    @staticmethod
    def setup():
        print "***** starting setup *****"
        # GPIO.setmode(GPIO.BCM)
        # GPIO.setup(22, GPIO.IN)  # button for street A traffic detect(TA)
        # GPIO.setup(17, GPIO.IN)  # button for street B traffic detect(TB)
        # GPIO.setup(25, GPIO.OUT)  # green light on street A
        # GPIO.output(25, 1)
        # GPIO.setup(24, GPIO.OUT)  # red light on street A
        # GPIO.output(24, 0)
        # GPIO.setup(23, GPIO.OUT)  # green light on street B
        # GPIO.output(23, 0)
        # GPIO.setup(18, GPIO.OUT)  # red light on street B
        # GPIO.output(18, 1)

    @staticmethod
    def flash():
        GpioCtrl.n = 0
        print "now GpioCtrl.n is {0}".format(GpioCtrl.n)
        # GPIO.output(25, 1)
        # GPIO.output(23, 1)
        # sleep(0.5)
        # GPIO.output(25, 0)
        # GPIO.output(23, 0)
        # sleep(0.5)
        # GPIO.output(25, 1)
        # GPIO.output(23, 1)
        # sleep(0.5)
        # GPIO.output(25, 0)
        # GPIO.output(23, 0)
        # sleep(0.5)
        # GPIO.output(25, 1)
        # GPIO.output(23, 1)
        # sleep(0.5)
        # GPIO.output(25, 0)
        # GPIO.output(23, 0)
        # sleep(0.5)
        # GPIO.output(25, 1)
        # GPIO.output(23, 1)
        # sleep(0.5)
        # GPIO.output(25, 0)
        # GPIO.output(23, 0)
        # sleep(0.5)
        # GPIO.output(25, 1)
        # GPIO.output(23, 1)
        # sleep(0.5)
        # GPIO.output(25, 0)
        # GPIO.output(23, 0)
        # sleep(0.5)

    @staticmethod
    def tick():
        if (GpioCtrl.interruptFlag == 0):
            sleep(0.1)
            GpioCtrl.interruptFlag = 1

    @staticmethod
    def display(lights):
        print "displaying is {0}".format(lights)
        # GPIO.output(25, lights[0])
        # GPIO.output(24, lights[1])
        # GPIO.output(23, lights[2])
        # GPIO.output(18, lights[3])


class Traffic(object):
    """docstring for Traffic"""

    def __init__(self, tfk_name, redOn):
        super(Traffic, self).__init__()
        self.tfk_name = tfk_name
        self.redOn = redOn
        self.btn = 0
        self.btnLast = 0
        self.trafficWon = 0
        self.lights = [0, 0, 0, 0]

    def standBy(self, other):
        if self.trafficWon == 1 and self.redOn == 1:
            GpioCtrl.flash()
            GpioCtrl.display(self.lights)
            self.trafficWon, other.trafficWon = 0, 0
            self.redOn, other.redOn = not self.redOn, not other.redOn

    def traffic_check(self, other):
        if self.trafficWon == 1 and self.redOn == 1:
            GpioCtrl.flash()
            GpioCtrl.display(self.lights)
            self.trafficWon, other.trafficWon = 0, 0
            self.redOn, other.redOn = not self.redOn, not other.redOn

    def displayInfo(self):
        print "tfk_name:{0}, redOn:{1}, btn:{2}, btnLast:{3}, trafficWon:{4}".format(self.tfk_name, self.redOn, self.btn, self.btnLast, self.trafficWon)

    def operation(self, other):
        GpioCtrl.n = GpioCtrl.n + 1
        if GpioCtrl.n > 100:
            standBy(self, other)
        elif GpioCtrl.n == 100:
            traffic_check(self, other)

    def setBtn(self, pin):
        btn_old = GPIO.input(pin)
        sleep(0.06)
        self.btn = GPIO.input(pin)
        if (self.btn != btn_old):
            self.btn = btn_old

if __name__ == '__main__':
    t1 = Traffic("t1", 1)
    t2 = Traffic("t2", 0)
    # init t1
    t1.lights = [1, 0, 0, 1]
    # init t2
    t2.lights = [0, 1, 1, 0]
    while True:
        t1.btnLast, t2.btnLast = 0, 0
        t1.setBtn(22)
        t2.setBtn(17)
        if ((t1.btnLast == 0) and (t1.btn == 1)):
            t1.trafficWon = 1
            print('button T1 pressed')
        elif ((t2.btnLast == 0) and (t2.btn == 1)):
            t2.trafficWon = 1
            print('button T2 pressed')
        GpioCtrl.tick()
        if GpioCtrl.interruptFlag == 1:
            t1.operation(t2)
