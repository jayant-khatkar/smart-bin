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
	num = input('enter num:')#python3 uses input(),p2 uses raw_input()

	if num == 'a':
# COMZ PROTOCOL: DISTANCE AND ANGLE OFFSETTED BY 100.
		bt_send(bluetooth, 100190)	#order: distangle
		time.sleep(1)
	num2 = input('enter num2: ')
	if num2 == 'a':
		bt_send(bluetooth, 110190)
		time.sleep(1)
	num3 = input('enter num3: ')
	if num3 == 'a':
		bt_send(bluetooth, 110235)
		time.sleep(1)
	num4 = input('enter num4: ')
	if num4 == 'a':
		bt_send(bluetooth, 110460)
		time.sleep(1)
	num5 = input('enter num5: ')
	if num5 == 'a':
		bt_send(bluetooth, 110460)
		time.sleep(0)
	bluetooth.close()
	
			




