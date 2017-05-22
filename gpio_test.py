
# script turns on and off a selected pin.


import RPi.GPIO as GPIO
import time


print "HERE WEEE GOOO!"

pin = 18
pin_ref_volt = 23


GPIO.setmode(GPIO.BCM) # set board mode to broad com
GPIO.setup(pin, GPIO.OUT) # set up pin as output

#below sets up a random 3.3V reference pin. needed to convert 3.3V to 5V
GPIO.setup(pin_ref_volt, GPIO.OUT)
GPIO.output(pin_ref_volt, GPIO.HIGH)
try:	
	while True:		
		GPIO.output(pin,GPIO.HIGH) #turn on pin 18
		print 'up'	
		time.sleep(1) #delay for 1 sec
		GPIO.output(pin,GPIO.LOW)#turn off pin 18
		print 'down'
		time.sleep(1)
except KeyboardInterrupt:
	GPIO.cleanup()
	print '\nClean them pins'




