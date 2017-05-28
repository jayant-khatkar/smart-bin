
# attempt at making a client that will poll forever

import socket
import sys

def read(port):
        s = socket.socket()


        host = '192.168.2.9'
        s.connect((host,port))


        try:
                msg = s.recv(1024)
        #       print (msg.decode('ascii'))
                s.close()
        except socket.error, msg:
                sys.stderr.write('error %s'%msg[1])
                s.close()
                print 'close'
                sys.exit(2)
        return msg

def process(data):
	

def servo_actuate(angle):
	return

def motor_actuate(range):
	return

if __name__ == '__main__':
        
	# initalise variables
	port = 1025

	while True:
		data = read(port)
		range, angle = process(data)	
		servo_actuate(angle)
		motor_actuate(range)		

