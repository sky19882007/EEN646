#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
from time import sleep
# import RPi.GPIO as GPIO


class Traffic(object):
    """docstring for Traffic"""

    def __init__(self):
        super(Traffic, self).__init__()
        self.redtime = 8
        self.greentime = 5
        self.ytime = 3
        self.cclor = 0
        self.ctime = 1
        self.sleepCnt = 0

    def checkStatus(self):
        if self.cclor == 0 and self.ctime >= self.redtime:
            print "change color"

if __name__ == '__main__':
    t = Traffic()
    while True:
        t.checkStatus()
        sleep(1)
        t.ctime = t.ctime + 1
        t.sleepCnt = t.sleepCnt + 1
        print "t.sleepCnt is {0}".format(t.sleepCnt)
        key = raw_input("intrupt?")
        if key:
            t.ctime = t.redtime - 2
