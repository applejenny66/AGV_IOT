# car.py
import time
import RPi.GPIO as GPIO
import numpy as np
from adafruit_motorkit import MotorKit
#from picamera.array import PiRGBArray
#from picamera import PiCamera
#from PIL import Image

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
        #self.camera = PiCamera()
        
        time.sleep(0.1)

    def angle_to_duty_cycle(self, angle=0):
        if (50 <= angle <= 110):
            GPIO.output(self.CONTROL_PIN, True)
            dc = (0.05 * self.PWM_FREQ) + (0.19 * self.PWM_FREQ * angle / 180)
            self.pwm.ChangeDutyCycle(dc)
            time.sleep(0.3)
            GPIO.output(self.CONTROL_PIN, False)
    
    def straight(self):
        self.angle_to_duty_cycle(91)

    def turn_left(self):
        self.angle_to_duty_cycle(50) #50

    def turn_right(self):
        self.angle_to_duty_cycle(100) #110

    def forward(self):
        self.kit.motor1.throttle = 0.9

    def stop(self):
        self.kit.motor1.throttle = 0

    def backfard(self):
        self.kit.motor1.throttle = -0.9

    def set_throttle(self, value):
        self.kit.motor1.throttle = value



def route_1():
    car_ = car()
    car_.straight()
    time.sleep(0.2)
    car_.forward()
    time.sleep(1.1)

    car_.turn_left()
    time.sleep(0.5)
    car_.turn_right()
    time.sleep(0.5)
    car_.straight()
    time.sleep(1)
    car_.turn_left()
    time.sleep(0.5)
    car_.stright()
    time.sleep(0.5)
    car_.turn_right()
    time.sleep(0.5)
    car_.straight()
    time.sleep(2)
    car_.stop()

    print ("finished")


if __name__ == "__main__":
    route_1()

"""
if __name__ == "__main__":
    car_test = car()
    car_test.straight()
    time.sleep(1)
    car_test.forward()
    time.sleep(3)
    car_test.stop()
    time.sleep(0.5)
    car_test.turn_left()
    car_test.set_throttle(0.2)
    time.sleep(2)
    car_test.stop()
"""


