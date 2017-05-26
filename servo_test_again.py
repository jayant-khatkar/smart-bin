import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(26,GPIO.OUT)

try:
	while True:
		GPIO.output(26,1)
		time.sleep(0.0015)
		GPIO.output(26,0)

		time.sleep(2)

except KeyboardInterrupt:
	GPIO.cleanup()

