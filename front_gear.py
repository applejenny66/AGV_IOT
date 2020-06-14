import RPi.GPIO as GPIO
import time
CONTROL_PIN = 17
PWM_FREQ = 50
STEP = 15

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(CONTROL_PIN, GPIO.OUT)

pwm = GPIO.PWM(CONTROL_PIN, PWM_FREQ)
pwm.start(0)

def angle_to_duty_cycle(angle=0):
    if 50<=angle<=110:
        GPIO.output(CONTROL_PIN, True)
        dc = (0.05 * PWM_FREQ) + (0.19 * PWM_FREQ * angle / 180)
        pwm.ChangeDutyCycle(dc)
        time.sleep(1)
        GPIO.output(CONTROL_PIN, False)
def turn_left():
    angle_to_duty_cycle(50)
def turn_right():
    angle_to_duty_cycle(110)
turn_left()