# from www.instructables.com/id/Read-and-write-from-serial-port-with-Raspberry-Pi/
#file reads something on the ttyAMA0 port
# TO RUN: this file needs to run at the same time as serial_write.py


import time
import serial

ser = serial.Serial(

	port='/dev/ttyAMA0',
	baudrate = 9600,
	parity = serial.PARITY_NONE,
	stopbits = serial.STOPBITS_ONE,
	bytesize = serial.EIGHTBITS,
	timeout = 1
)
counter = 0

while 1:
	x = ser.readline()
	print x

