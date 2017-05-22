# code taken from d2rk.blogspot.com.au/2013/run-sabertooth-2x5-in-simplified-serial.html

import serial

SABERTOOTH_PORT_NAME = '/dev/ttyAMA0'
SABERTOOTH_PORT_BAUDRATE = 9600
SABERTOOTH_PORT_BYTESIZE = 8


sabertooth = serial.Serial(port = SABERTOOTH_PORT_NAME,
			baudrate = SABERTOOTH_PORT_BAUDRATE,
			bytesize = SABERTOOTH_PORT_BYTESIZE,
			parity = serial.PARITY_NONE,
			writeTimeout = 0,
			stopbits = serial.STOPBITS_ONE,
			dsrdtr = True)

if sabertooth is None:
	print 'oops'
print 'sabertooth initialized'

try:
	while True:
		cmd = chr(100)
		sabertooth.write(cmd)
		sabertooth.flush()
except KeyboardInterrupt:
	sabertooth.close()






