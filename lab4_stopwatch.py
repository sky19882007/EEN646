import time
from time import sleep

import RPi.GPIO as GPIO
from Adafruit_7Segment import SevenSegment

segment = SevenSegment(address=0x70)

# setup function


def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(25, GPIO.OUT)      # set output pin 25 as the status LED
    GPIO.setup(22, GPIO.IN)       # set input pin 22 as the start/stop switcher
    GPIO.setup(17, GPIO.IN)       # set input pin 17 as the reset switcher
    global n
    n = 0
    global _n
    _n = 0
    global encount                # button counter
    encount = 0
    global interruptFlag
    interruptFlag = 0


def isr():
    global n
    global interruptFlag
    global _n
    n = _n / 10
    if n > 5999:
        print('reach memery cap and reset timer back to 0')
        n = 0
        _n = 0
    interruptFlag = 0


def tick():
    global _n
    global interruptFlag
    if(interruptFlag == 0):
        sleep(0.1)
        _n = _n + 1
        interruptFlag = 1


def startStop_debounce():
    startStop_old = GPIO.input(22)  # pin 22 is start/stop button
    sleep(0.06)
    startStop = GPIO.input(22)
    if(startStop == startStop_old):
        return startStop
    else:
        return startStop_old


def reset_debounce():
    reset_old = GPIO.input(17)  # pin 17 is reset button
    sleep(0.06)
    reset = GPIO.input(17)
    if(reset == reset_old):
        return reset
    else:
        return reset_old

# Main function
setup()
global encount
global n
global _n
while True:
    startStop = startStop_debounce()
    reset = reset_debounce()
    if(startStop == True):
        encount = encount + 1
        print('start/stop button pressed: %d' % encount)
    if(reset == True):
        n = 0
        _n = 0
        # update 7 segement display
        segment.writeDigit(0, 0)
        segment.writeDigit(1, 0)
        segment.writeDigit(2, 0)
        segment.writeDigit(3, 0)
        segment.writeDigit(4, 0)
    if((encount & 1) == 1):
        GPIO.output(25, 1)           # turn on the status light on pin 25
        tick()
    else:
        GPIO.output(25, 0)           # turn off the status light on pin 25
    # update 7 segement display
    segment.writeDigit(0, (n / 60) / 10)
    segment.writeDigit(1, (n / 60) % 10)
    segment.writeDigit(2, n % 2)
    segment.writeDigit(3, (n % 60) / 10)
    segment.writeDigit(4, (n % 60) % 10)
    if(interruptFlag == 1):
        isr()
