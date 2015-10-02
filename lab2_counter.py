# Lab 2 

import time
from time import sleep
import RPi.GPIO as GPIO

# setup GPIO function and GPIO pin


def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    # status LED, output signal shows startstop status
    GPIO.setup(4, GPIO.OUT)

    # input signal, startstop button and reset button
    GPIO.setup(17, GPIO.IN)
    GPIO.setup(22, GPIO.IN)

    # 4 data LEDs, output signal
    GPIO.setup(25, GPIO.OUT)
    GPIO.setup(24, GPIO.OUT)
    GPIO.setup(23, GPIO.OUT)
    GPIO.setup(18, GPIO.OUT)

    # counter
    global n
    n = 0


def count():
    global n
    n = n + 1
    if n == 16:
        n = 0
    sleep(1)

# Main function
if __name__ == '__main__':
    setup()
    while True:
        startStop = GPIO.input(17)
        reset = GPIO.input(22)
        # when startstop button is pressed system will begin counting.
        if(startStop == True):
            GPIO.output(4, 1)
            count()
            # one light will be select to be turn on
            lightOn = n % 4
            if(lightOn == 0):
                GPIO.output(25, 1)
            else:
                GPIO.output(25, 0)
            if(lightOn == 1):
                GPIO.output(24, 1)
            else:
                GPIO.output(24, 0)
            if(lightOn == 2):
                GPIO.output(23, 1)
            else:
                GPIO.output(23, 0)
            if(lightOn == 3):
                GPIO.output(18, 1)
            else:
                GPIO.output(18, 0)
        # when startstop is not pressed the system will stay stop, the status LED will keep off.
        else:
            GPIO.output(4, 0)
            # when reset button is pressed n will be reset to be 0 and GPIO will be clean up.
            if(reset == True):
                n = 0
            # display count
            d0 = n & 8
            d1 = n & 4
            d2 = n & 2
            d3 = n & 1
            GPIO.output(25, d0)
            GPIO.output(24, d1)
            GPIO.output(23, d2)
            GPIO.output(18, d3)
