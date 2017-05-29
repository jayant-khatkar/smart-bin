# attempt at making a client that will poll forever

import socket
import sys

def read(port):
	s = socket.socket()

	
	host = '172.17.33.125'# (172.. is Pi's IP, '10.19.92.44' is macs)
	s.connect((host,port))

	
	try:
		msg = s.recv(1024)
	#	print (msg.decode('ascii'))
		s.close()
	except socket.error, msg:		
		sys.stderr.write('error %s'%msg[1])
		s.close()
		print 'close'
		sys.exit(2)
	return msg

if __name__ == '__main__':
	port = 1025
	while True:
		print 'hey, checking TCP socket'
		data = read(port)
		port = port + 1
		print 'i just read %s' % data
		print 'port num is: %d' % port	
	


