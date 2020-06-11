# car.py
import time
import RPi.GPIO as GPIO
import numpy as np
from adafruit_motorkit import MotorKit
from picamera.array import PiRGBArray
from picamera import PiCamera
from PIL import Image

class car:
    def __init__(self):
        self.kit = MotorKit()
        self.CONTROL_PIN = 17
        self.PWM_FREQ = 50
        self.STEP = 15

        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.CONTROL_PIN, GPIO.OUT)

        self.pwm = GPIO.PWM(self.CONTROL_PIN, self.PWM_FREQ)
        self.pwm.start(0)
        self.camera = PiCamera()
        
        time.sleep(0.1)


    def forward(self):
        self.kit.motor1.throttle = 1.0

    def stop(self):
        self.kit.motor1.throttle = 0

    def backfard(self):
        self.kit.motor1.throttle = -1.0

    def set_throttle(self, value):
        self.kit.motor1.throttle = value

    def angle_to_duty_cycle(self, angle=0):
        self.duty_cycle = (0.05 * self.PWM_FREQ) + \
            (0.19 * self.PWM_FREQ * angle / 180)
        return (self.duty_cycle)

    def capture(self, rawCapture):
        self.camera.capture(rawCapture, format="bgr")
        image = rawCapture.array
        print ("image shape: ", image.shape)
        #(1080, 1920, 3)

        new_im = Image.fromarray(image)
        new_im.save("test.png")
        resize_im = Image.open("test.png")
        resize_im = resize_im.resize((192, 108))
        resize_im.save("test_resize.png")
        return image, resize_im

if __name__ == "__main__":
    car = car()
    angle =  50
    #dc = car.angle_to_duty_cycle(angle)
    #car.pwm.ChangeDutyCycle(dc)
    rawCapture = PiRGBArray(car.camera)
    image, resize_im = car.capture(rawCapture)
    #print ()
