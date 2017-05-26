import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
servoPin = 26
frequency = 50 #Hz
GPIO.setup(servoPin,GPIO.OUT)
pwm = GPIO.PWM(servoPin,frequency)
pwm.start(6.5)
max_duty = 12
min_duty = 2
duty_range = max_duty - min_duty

for i in range(0,30):
	desiredPosition = input("Where do you want the servo?")
	DC = (95./1800.)*desiredPosition+min_duty
	pwm.ChangeDutyCycle(DC)
pwm.stop()
GPIO.cleanup()


