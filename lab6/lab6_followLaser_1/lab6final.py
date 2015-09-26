from SimpleCV import Camera, Color, Display, Image
#import serial
import time

cam = Camera(prop_set={'width': 320, 'height': 240})

# ser=serial.Serial('/dev/ttyUSB0',9600,timeout=1)
# ser.open()

while True:
    img = cam.getImage()
    dist = img.colorDistance(Color.BLACK).dilate(2)
    segmented = dist.stretch(200, 255)  # .erode(1).dilate(3) #.erode(2)
    # blobs = segmented.findBlobs(minsize=16,maxsize=625)  #size: 2x2 - 16x16
    blobs = segmented.findBlobs()
    if blobs:
        circles = blobs.filter([b.isCircle(0.55) for b in blobs])
        if circles:
            X = circles[-1].x
            Y = circles[-1].y
            if(X > 10 and X < 310 and Y > 10 and Y < 230):
                #img[(X-10):(X+10),Y] = Color.BLACK
                img[X, (Y - 10):(Y + 10)] = Color.BLACK
                if X < 160:
                    X = 160 - X
                else:
                    X = X - 160
                # ser.write(chr(X))
                print "sending X=%d" % X
    img.show()
