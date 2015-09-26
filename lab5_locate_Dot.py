from SimpleCV import *
from time import sleep

display = Display(resolution=(320, 240))
cam = Camera(prop_set={'width': 320, 'height': 240})
while display.isNotDone():
    img = cam.getImage()
    dist = img.colorDistance(SimpleCV.Color.BLACK).dilate(2)
    segmented = dist.stretch(200, 255)
    blobs = segmented.findBlobs()
    if blobs:
        circles = blobs.filter([b.isCircle(0.55) for b in blobs])
        if circles:
            img.drawCircle((circles[-1].x, circles[-1].y), circles[-1].radius(), Color.BLUE, 3)
            X = circles[-1].x
            Y = circles[-1].y
            print(X, Y)
            img[X, Y] = Color.BLACK
            if(X > 10 and X < 310 and Y > 10 and Y < 230):
                img[(X - 10):(X + 10), Y] = Color.BLACK
                img[X, (Y - 10):(Y + 10)] = Color.BLACK
    img.show()
    sleep(0.1)
