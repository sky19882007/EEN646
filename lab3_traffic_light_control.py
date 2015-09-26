import time
from time import sleep
import RPi.GPIO as GPIO


def setup():
    global n
    n = 0
    global Red_on_A  # status on street A: 1 is blocked, 0 is not blocked
    Red_on_A = 0
    global Red_on_B  # status on street B: 1 is blocked, 0 is not blocked
    Red_on_B = 1
    global interruptFlag
    interruptFlag = 0
    global TA_button
    TA_button = 0
    global TB_button
    TB_button = 0
    global TA_button_end
    TA_button_end = 0
    global TB_button_end
    TB_button_end = 0
    global TrafficWon_A  # traffic on street A is waiting
    TrafficWon_A = 0
    global TrafficWon_B  # traffic on street B is waiting
    TrafficWon_B = 0

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(22, GPIO.IN)  # button for street A traffic detect(TA)
    GPIO.setup(17, GPIO.IN)  # button for street B traffic detect(TB)
    GPIO.setup(25, GPIO.OUT)  # green light on street A
    GPIO.output(25, 1)
    GPIO.setup(24, GPIO.OUT)  # red light on street A
    GPIO.output(24, 0)
    GPIO.setup(23, GPIO.OUT)  # green light on street B
    GPIO.output(23, 0)
    GPIO.setup(18, GPIO.OUT)  # red light on street B
    GPIO.output(18, 1)


def isr():
    global n
    global interruptFlag
    n = n + 1
    print(n / 10)
    operation_check()


def operation_check():
    global TrafficWon_A  # traffic on street A is waiting
    global TrafficWon_B  # traffic on street B is waiting
    if (n > 100):
        Standby()
    elif n == 100:
        Traffic_check()


def Standby():
    global TrafficWon_A  # traffic on street A is waiting
    global TrafficWon_B  # traffic on street B is waiting
    global Red_on_B
    global Red_on_A
    print('standby')

    if (TrafficWon_A == 1 and Red_on_A == 1):
        flash()
        GPIO.output(25, 1)
        GPIO.output(24, 0)
        GPIO.output(23, 0)
        GPIO.output(18, 1)
        TrafficWon_A = 0
        TrafficWon_B = 0
        Red_on_A = not Red_on_A
        Red_on_B = not Red_on_B
    if (TrafficWon_B == 1 and Red_on_B == 1):
        flash()
        GPIO.output(25, 0)
        GPIO.output(24, 1)
        GPIO.output(23, 1)
        GPIO.output(18, 0)
        TrafficWon_A = 0
        TrafficWon_B = 0
        Red_on_A = not Red_on_A
        Red_on_B = not Red_on_B


def Traffic_check():
    global TrafficWon_A  # traffic on street A is waiting
    global TrafficWon_B  # traffic on street B is waiting
    global Red_on_B
    global Red_on_A
    print('Traffic_checking')
    if (TrafficWon_A == 1 and Red_on_A == 1):
        flash()
        GPIO.output(25, 1)
        GPIO.output(24, 0)
        GPIO.output(23, 0)
        GPIO.output(18, 1)
        TrafficWon_A = 0
        TrafficWon_B = 0
        Red_on_A = not Red_on_A
        Red_on_B = not Red_on_B
    if (TrafficWon_B == 1 and Red_on_B == 1):
        flash()
        GPIO.output(25, 0)
        GPIO.output(24, 1)
        GPIO.output(23, 1)
        GPIO.output(18, 0)
        TrafficWon_A = 0
        TrafficWon_B = 0
        Red_on_A = not Red_on_A
        Red_on_B = not Red_on_B


def tick():
    global interruptFlag
    if (interruptFlag == 0):
        sleep(0.1)
        interruptFlag = 1


def flash():
    global n
    n = 0
    GPIO.output(25, 1)
    GPIO.output(23, 1)
    sleep(0.5)
    GPIO.output(25, 0)
    GPIO.output(23, 0)
    sleep(0.5)
    GPIO.output(25, 1)
    GPIO.output(23, 1)
    sleep(0.5)
    GPIO.output(25, 0)
    GPIO.output(23, 0)
    sleep(0.5)
    GPIO.output(25, 1)
    GPIO.output(23, 1)
    sleep(0.5)
    GPIO.output(25, 0)
    GPIO.output(23, 0)
    sleep(0.5)
    GPIO.output(25, 1)
    GPIO.output(23, 1)
    sleep(0.5)
    GPIO.output(25, 0)
    GPIO.output(23, 0)
    sleep(0.5)
    GPIO.output(25, 1)
    GPIO.output(23, 1)
    sleep(0.5)
    GPIO.output(25, 0)
    GPIO.output(23, 0)
    sleep(0.5)


def debounce_TA():
    TA_button_old = GPIO.input(22)
    sleep(0.06)
    TA_button = GPIO.input(22)
    if (TA_button == TA_button_old):
        return TA_button
    else:
        return TA_button_old


def debounce_TB():
    TB_button_old = GPIO.input(17)
    sleep(0.06)
    TB_button = GPIO.input(17)
    if (TB_button == TB_button_old):
        return TB_button
    else:
        return TB_button_old

# Main
setup()
while True:
    global TA_button_last
    TA_button_last = 0
    global TB_button_last
    TB_button_last = 0
    global TrafficWon_A
    global TrafficWon_B
    TA_button = debounce_TA()
    TB_button = debounce_TB()
    if ((TA_button_last == 0) and (TA_button == 1)):
        TrafficWon_A = 1
        print('button TA pressed')
    elif ((TB_button_last == 0) and (TB_button == 1)):
        TrafficWon_B = 1
        print('button TB pressed')
    tick()
    if (interruptFlag == 1):
        isr()
