import time

from adafruit_motorkit import MotorKit

kit = MotorKit()

kit.motor1.throttle = -0.5
time.sleep(2)
kit.motor1.throttle = 0
