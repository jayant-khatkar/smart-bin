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
		bt_send(bluetooth, 150100)      #order: distangle
		time.sleep(1)
	num2 = raw_input('enter num2: ')
	if num2 == 'a':
		bt_send(bluetooth, 150145)
		time.sleep(1)
	num3 = raw_input('enter num3: ')
	if num3 == 'a':
		bt_send(bluetooth, 150190)
		time.sleep(1)
	num4 = raw_input('enter num4: ')
	if num4 == 'a':
		bt_send(bluetooth, 150235)
		time.sleep(1)
	num5 = raw_input('enter num5: ')
	if num5 == 'a':
		bt_send(bluetooth, 150280)
		time.sleep(0)
	bluetooth.close()
