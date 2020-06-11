
from picamera.array import PiRGBArray

from picamera import PiCamera
from time import sleep
import cv2 as cv
import time

camera = PiCamera()
rawCapture = PiRGBArray(camera)

#cap = camera.start_preview()
sleep(0.1)

camera.capture(rawCapture, format="bgr")
image = rawCapture.array
cv2.imshow("image", image)
cv2.waitkey(0)

#while True:
#    pass

#sleep(5)
#cap.stop_preview()
#camera.stop_preview()
