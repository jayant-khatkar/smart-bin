import pygame, sys, time
from pygame.locals import *

pygame.init()
pygame.joystick.init()
joystick = pygame.joystick.Joystick(0)
joystick.init()
screen = pygame.display.set_mode((400,300))
pygame.display.set_caption('Hello World!')

interval = 0.01

joystick_count = pygame.joystick.get_count()
print("joystick_count")
print(joystick_count)
print("-------------")

numaxes = joystick.get_numaxes()
print("numaxes")
print(numaxes)
print("-------------")

numbuttons = joystick.get_numbuttons()
print("numbuttons")
print(numbuttons)
print("-------------")

loopQuit = False
while loopQuit == False:
	outstr = ""
	
	for i in range(0,1):
		axis=joystick.get_axis(i)
		outstr = outstr + str(i) + ":" + str(axis) + "|"
	print(outstr)


	for event in pygame.event.get():
		if event.type == QUIT:
			loopQuit = True
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				loopQuit = True


	time.sleep(interval)

pygame.quit()
sys.exit()
