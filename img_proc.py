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
        self.gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        kernel_size = 5
        self.blur_gray = cv2.GaussianBlur(gray, (kernel_size, kernel_size), 0)
        
        low_thres = 50
        high_thres = 150
        edges = cv2.Canny(self.blur_gray, low_thres, hogh_thres)
        
        rho = 1
        theta = np.pi / 180
        threshold = 15
        min_line_length = 50
        max_line_gap = 20
        
        line_image = np.copy(self.img) * 0
        
        lines = cv2.HoughLinesP(edges, rho, theta, threshold, np.array([]),\
                min_line_length, max_line_gap)

        for line in lines:
            for x1, y1, x2, y2 in line:
                cv2.line(line_image, (x1, y1), (x2, y2), (255, 0, 0), 5)

        lines_edges = cv2.addWeighted(self.img, 0.8, line_image, 1, 0)
        cv2.imwrite("line.png", lines_edges)


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
