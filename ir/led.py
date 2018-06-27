import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.OUT)
GPIO.setup(13, GPIO.OUT)

def toggle_led(runKey):
    if runKey == 'right':
        GPIO.output(11, True)
        GPIO.output(13, False)
    elif runKey == 'left':
        GPIO.output(11, False)
        GPIO.output(13, True)
    else:
        GPIO.output(11, False)
        GPIO.output(13, False)