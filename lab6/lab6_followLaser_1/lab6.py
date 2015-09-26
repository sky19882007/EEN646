from SimpleCV import Camera, Color, Display, Image
import serial
import time
from time import sleep

cam = Camera(prop_set={'width': 320, 'height': 240})

ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
ser.open()

sleep(5)
while True:
    img = cam.getImage()
    dist = img.colorDistance(Color.BLACK).dilate(2)
    segmented = dist.stretch(200, 255)
    blobs = segmented.findBlobs()
    if blobs:
        circles = blobs.filter([b.isCircle(0.45) for b in blobs])
        if circles:
            X = circles[-1].x
            if X > 32 and X < 288:
                print "sending X=%d" % (X - 32)
                ser.write(chr(X - 32))
