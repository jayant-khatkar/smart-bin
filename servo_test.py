import RPi.GPIO as GPIO

import time

GPIO.setmode(GPIO.BCM)

GPIO.setup(26,GPIO.OUT)

frequencyHertz = 50
pwm = GPIO.PWM(26, frequencyHertz)

leftPosition = 0.75
rightPosition = 2.5
middlePosition = (rightPosition - leftPosition) / 2 + leftPosition

positionList = [leftPosition, middlePosition, rightPosition, middlePosition]

msPerCycle = 1000/frequencyHertz

for i in range(3):

	for position in positionList:
		dutyCyclePercentage = position*100/msPerCycle
		print "Position: " + str(position)
		print "Duty Cycle:" + str(dutyCyclePercentage) + "%"
		print ""
		pwm.start(dutyCyclePercentage)
		time.sleep(.5)

pwm.stop()

GPIO.cleanup()

