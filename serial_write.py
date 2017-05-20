#from www.instructables.com/id/Read-and-write-from-serial-port-with-Raspberry-Pi/
#file writes something on ttyAMA0 port
#TO RUN: this file needs to run at the same time as serial_read.py	


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
counter = 0

while 1:
	ser.write('Write counter: %d \n' %(counter))
	time.sleep(1)
	counter+=1


