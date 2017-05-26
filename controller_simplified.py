import pygame, sys, time
import RPi.GPIO as GPIO
from pygame.locals import *

GPIO.setmode(GPIO.BCM)
servoPin = 26
frequency = 50 #Hz
GPIO.setup(servoPin,GPIO.OUT)
pwm = GPIO.PWM(servoPin,frequency)
pwm.start(6.5)
max_duty = 12
min_duty = 2
duty_range = max_duty - min_duty


pygame.init()
pygame.joystick.init()
joystick = pygame.joystick.Joystick(0)
joystick.init()
screen = pygame.display.set_mode((400,300))
pygame.display.set_caption('Hello World')

interval = 0.05

loopQuit = False
while loopQuit == False:
        outstr = ""
	angle=0
        for i in range(0,1):
                x0=joystick.get_axis(i)
		x1=joystick.get_axis(i+1)
		
		if  x1<-0.98:
			angle = 45*x0
		elif x1>0.98:
			angle = -x0*45+180
		elif x0>0.98:
			angle = x1*45 +90
		elif x0<-0.98:
			angle = -x1*45+270

	angle = round(angle)
	print angle        

	desiredPosition = angle
        DC = (95./1800.)*desiredPosition+min_duty
        pwm.ChangeDutyCycle(DC)



        for event in pygame.event.get():
                if event.type == QUIT:
                        loopQuit = True
                elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                                loopQuit = True



        time.sleep(interval)

pwm.stop()
GPIO.cleanup()
pygame.quit()
sys.exit()


