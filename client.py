#FROM http://www.tutorialspoint.com/python/python_networking.htm
#CLIENT
import socket               # Import socket module

s = socket.socket()         # Create a socket object
#host = socket.gethostname() # Get local machine name
port = 9999                # Reserve a port for your service.
host = '192.168.2.9'		#ip address of server
s.connect((host, port))

msg = s.recv(1024)
s.close()

print (msg.decode('ascii'))
