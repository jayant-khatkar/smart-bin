
# script turns on and off a selected pin.


import RPi.GPIO as GPIO
import time


print "HERE WEEE GOOO!"

pin = 18

GPIO.setmode(GPIO.BCM) # set board mode to broad com
GPIO.setup(pin, GPIO.OUT) # set up pin as output

try:	
	while True:		
		GPIO.output(pin,GPIO.HIGH) #turn on pin 18
		print 'up'	
		time.sleep(1) #delay for 1 sec
		GPIO.output(pin,GPIO.LOW)#turn off pin 18
		time.sleep(1)
		print ('down')
except KeyboardInterrupt:
	GPIO.cleanup()
	print '\nClean them pins'




