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
if ser is None:
	print 'Sabertooth not found'
	 
print 'sabertooth initialized'

command = chr(127) # this value should move motor 1 at half speed
'''
ser.write(command)
#ser.flush()
time.sleep(10)
ser.flush()
ser.write(chr(0))
ser.flush()
ser.close()
print 'end'
'''
try:
	while True:
		ser.write(command)
		ser.flush() # flush of file like objects. in this case, wait until all data is written.
#		time.sleep(2)
except KeyboardInterrupt:
	ser.write(chr(0))
	ser.flush()
	ser.close()
	print 'end'

#print 'end'
#ser.write('%d' % (command))
#time.sleep(2)
#ser.write('%d' % (command))
#time.sleep(2)

