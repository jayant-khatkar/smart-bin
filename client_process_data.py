st login: Sun May 28 19:45:08 on ttys000
sig:~ Alex$ ls
Desktop		Downloads	Movies		Pictures	smart-bin
Documents	Library		Music		Public
sig:~ Alex$ cd Desktop/
sig:Desktop Alex$ pwd
/Users/Alex/Desktop
sig:Desktop Alex$ ls
mac support for itunes login.rtf
sig:Desktop Alex$ cd ..
sig:~ Alex$ ls
Desktop		Downloads	Movies		Pictures	smart-bin
Documents	Library		Music		Public
sig:~ Alex$ cd smart-bin/
sig:smart-bin Alex$ ls
README.md		main.py			sample.py
client.py		netcat.py		server.py
client_forever.py	netcat.pyc		server_forever.py
helloGit		netcat_example.py
sig:smart-bin Alex$ vim client_forever.py 




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

