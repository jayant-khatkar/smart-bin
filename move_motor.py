# THIS SCRIPT IS THE FIRST ATTEMPT AT MOVING THE BIG DICK MOTOR
# must send a byte over serial

import time
import serial


ser = serial.Serial(
	port = '/dev/ttyAMA0',
	baudrate = 9600,
	parity = serial.PARITY_NONE,
	stopbits = serial.STOPBITS_ONE,
	bytesize = serial.EIGHTBITS,
	timeout = 1
)


command = 95 # this value should move motor 1 at half speed
while 1:
	ser.write('yo %d \n' % (command))
	time.sleep(1)

