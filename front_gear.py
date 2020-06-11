import RPi.GPIO as GPIO

CONTROL_PIN = 17
PWM_FREQ = 50
STEP = 15

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(CONTROL_PIN, GPIO.OUT)

pwm = GPIO.PWM(CONTROL_PIN, PWM_FREQ)
pwm.start(0)

def angle_to_duty_cycle(angle=0):
    duty_cycle = (0.05 * PWM_FREQ) + (0.19 * PWM_FREQ * angle / 180)
    return (duty_cycle)
angle =  50
dc = angle_to_duty_cycle(angle)
pwm.ChangeDutyCycle(dc)
