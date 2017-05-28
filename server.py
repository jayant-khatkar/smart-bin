# FROM http://www.tutorialspoint.com/python/python_networking.htm
#SERVER
import socket               # Import socket module

s = socket.socket()         # Create a socket object
host = socket.gethostname() # Get local machine name
#host = 192.168.2.4		# ip address of client
port = 9999                # Reserve a port for your service.
s.bind((host, port))        # Bind to the port
print host
s.listen(5)                 # Now wait for client connection.
while True:
   c, addr = s.accept()     # Establish connection with client.
   print 'Got connection from', addr
   c.send('Thank you for connecting yalla habbibi')
   c.close()                # Close the connection
