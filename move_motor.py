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


command = chr(120) # this value should move motor 1 at half speed
try:
	while 1:
		ser.write(command)
		ser.flush()
		time.sleep(2)
except KeyboardInterrupt:
	ser.close()
	print 'end'

#print 'end'
#ser.write('%d' % (command))
#time.sleep(2)
#ser.write('%d' % (command))
#time.sleep(2)

