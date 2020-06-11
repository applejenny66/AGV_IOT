#img_proc.py

import time
import RPi.GPIO as GPIO
from adafruit_motorkit import MotorKit
from picamera.array import PiRGBArray
from picamera import PiCamera
from PIL import Image

from car import car

class image_procseeing():
    def __init__(self, img):
        self.img = img
        #(1080, 1920, 3)

    def find_line(self):
        pass


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
