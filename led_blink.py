import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(17,GPIO.OUT)

for i in range(5):
    GPIO.output(17,True)
    print "ON"
    time.sleep(2)
    GPIO.output(17,False)
    print "OFF"
    time.sleep(2)

GPIO.cleanup()
