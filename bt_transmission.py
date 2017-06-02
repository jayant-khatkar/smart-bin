# creating 2 funcs. 1 to connect.1 to send
# TESTER SCRIPT FOR TESTING BLUE TOOTHS TIMINGS hunches!!!


import serial
import time

def bt_connect():
	port="/dev/tty.HC-05-DevB"
	bluetooth=serial.Serial(port, 9600)
	bluetooth.flushInput() #This gives the bluetooth a little kick
	return bluetooth

def bt_send(bluetooth, i):
	bluetooth.write(str.encode(str(i)))
	bluetooth.flushInput()

def bt_close(bluetooth):
	bluetooth.close()

if __name__ == '__main__':
	bluetooth = bt_connect()
	num = raw_input('enter num:')#python3 uses input(),p2 uses raw_input()
	if num == 'a':
# COMZ PROTOCOL: DISTANCE AND ANGLE OFFSETTED BY 100.
		bt_send(bluetooth, 310000)
		time.sleep(3)
#		bt_send(bluetooth, 350200)	
		bt_close(bluetooth)




