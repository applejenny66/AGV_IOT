#img_proc.py

import time
import RPi.GPIO as GPIO
from adafruit_motorkit import MotorKit
from picamera.array import PiRGBArray
from picamera import PiCamera
from PIL import Image
import cv2
import numpy as np
from car import car

class image_procseeing():
    def __init__(self, img):
        self.img = img
        #(1080, 1920, 3)

    def find_line(self):
        
        self.gray = cv2.cvtColor(np.float32(self.img), cv2.COLOR_BGR2GRAY)
        #kernel_size = 5
        #self.blur_gray = cv2.GaussianBlur(self.gray, (kernel_size, kernel_size), 0)
        self.edges = cv2.Canny(self.gray, 50, 150, apertureSize = 3)
        minLineLength = 100
        maxLineGap = 10
        lines = cv2.HoughLinesP(edges, 1, np.pi/180, 100, \
                minLineLength, maxLineGap)
        for x1, y1, x2, y2 in lines[0]:
            cv2.line(self.img, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.imwrite("line.png", self.img)


if __name__ == "__main__":
    car = car()
    angle =  50
    #dc = car.angle_to_duty_cycle(angle)
    #car.pwm.ChangeDutyCycle(dc)
    rawCapture = PiRGBArray(car.camera)
    image, resize_im = car.capture(rawCapture)

    #img = Image.open("test.png")
    #print ("img type: ", type(image))
    procs = image_procseeing(resize_im)
    print ("shape: ", procs.img.size)
    procs.find_line()
