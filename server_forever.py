#attempt at making server run forever


import socket
import time

def send(data, port):
	s = socket.socket()
#	host = socket.gethostname()


	s.bind(('', port))
#	print host
	s.listen(5)
	
	c, addr = s.accept()
	print 'Got connection from',addr
	c.send(data)
	c.close()

if __name__ == '__main__':
	port = 1025
	num = 1
	while True:
		print 'hey, sending data'
		words = 'yew cuz'	
		data = words + str(num)
		print 'send data: %s' % data
		send(data,port)
		port = port + 1
		#time.sleep(1)
		num = num + 1
		print 'port num is %d' % port	
