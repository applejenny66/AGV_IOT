import time
import RPi.GPIO as GPIO
import numpy as np
from adafruit_motorkit import MotorKit

from car import car

car_ = car()
car_.stop()
