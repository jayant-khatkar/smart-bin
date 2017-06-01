
# function for bluetooth coms
# THIS SCRIPT USES CLOSURES. IT WORKS BUT bt_transmission.py IS PROBABLY BETTER

import serial
import time



def bt_connect():
	port="/dev/tty.HC-05-DevB" 
	bluetooth = serial.Serial(port, 9600)
	bluetooth.flushInput()
	def bt_send(distance):
		bluetooth.write(str.encode(str(distance)))
		return
	return bt_send

if __name__ == '__main__':

	set_distance = bt_connect()
	set_distance(50)
	time.sleep(1)
	set_distance(1000)
	time.sleep(1)
	set_distance(134543)
	

