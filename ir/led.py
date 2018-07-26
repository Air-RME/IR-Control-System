import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
GPIO.setup(33, GPIO.OUT)
GPIO.setup(35, GPIO.OUT)
GPIO.setup(37, GPIO.OUT)


# DEMO
# 33right
# 35center
# 37left
def toggle_led(runKey):
    if runKey == 'right':
        GPIO.output(33, False)
        GPIO.output(35, True)
        GPIO.output(37, True)
    elif runKey == 'center':
        GPIO.output(33, True)
        GPIO.output(35, False)
        GPIO.output(37, True)
    elif runKey == 'left':
        GPIO.output(33, True)
        GPIO.output(35, True)
        GPIO.output(37, False)
    else:
        GPIO.output(33, True)
        GPIO.output(35, True)
        GPIO.output(37, True)
