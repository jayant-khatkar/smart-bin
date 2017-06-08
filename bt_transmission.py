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


	try:
		while True:
			input = raw_input("Enter dist and angle (3digits for both!):")
			print "you sent a distance of %s and an angle of %s \n" % (input[:3],input[3:])
			send_cmd = str(int(input[:3])+100) + str(int(input[3:])+100)
			print 'command is %s' % send_cmd
			bt_send(bluetooth, send_cmd)
	except KeyboardInterrupt:
		bluetooth.close()
		print "Finished"
		
'''        num = input('enter num:')#python3 uses input(),p2 uses raw_input()
        if num == 'a':
# COMZ PROTOCOL: DISTANCE AND ANGLE OFFSETTED BY 100.
		bt_send(bluetooth, 150100)	#order: distangle
		time.sleep(1)
	num2 = input('enter num2: ')
	if num2 == 'a':
		bt_send(bluetooth, 150145)
		time.sleep(1)
	num3 = input('enter num3: ')
	if num3 == 'a':
		bt_send(bluetooth, 150190)
		time.sleep(1)
	num4 = input('enter num4: ')
	if num4 == 'a':
		bt_send(bluetooth, 150235)
		time.sleep(1)
	num5 = input('enter num5: ')
	if num5 == 'a':
		bt_send(bluetooth, 150280)
		time.sleep(0)
	#bluetooth.close()
	
	'''		




