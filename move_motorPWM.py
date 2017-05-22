

#www.sourceforge.net/p/raspberry-gpio-python/wiki/PWM/

import RPi.GPIO as GPIO

pin = 24
GPIO.setmode(GPIO.BCM)
GPIO.setup(pin, GPIO.OUT)
motor = GPIO.PWM(pin, 100) # (pin, freq Hz)
motor.start(50) #duty cycle
random = 1
try:

	while True:
		random+=1		
except KeyboardInterrupt:
	GPIO.cleanup()

