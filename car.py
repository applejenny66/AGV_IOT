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
        self.angle_to_duty_cycle(85)

    def turn_left(self):
        self.angle_to_duty_cycle(60) #50

    def turn_right(self):
        self.angle_to_duty_cycle(100) #110

    def forward(self):
        self.kit.motor1.throttle = 0.3

    def stop(self):
        self.kit.motor1.throttle = 0

    def backfard(self):
        self.kit.motor1.throttle = -0.3

    def set_throttle(self, value):
        self.kit.motor1.throttle = value

    """
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
    """

if __name__ == "__main__":
    car_ = car()
    #angle =  50
    car_.straight()
    #car_.angle_to_duty_cycle(angle=85)
    time.sleep(1)
    car_.forward()
    time.sleep(4)
    car_.set_throttle(0.1)
    car_.angle_to_duty_cycle(angle=50)
    time.sleep(2)
    car_.straight()
    car_.forward()
    time.sleep(2.5)
    #car_.angle_to_duty_cycle(angle=110)
    #time.sleep(0.1)
    car_.stop()
    #car.pwm.ChangeDutyCycle(dc)
    #rawCapture = PiRGBArray(car.camera)
    #image, resize_im = car.capture(rawCapture)
