
# below is a extract from a sample exploit that
# interfaces with a tcp socket

from netcat import Netcat

# start a new Netcat() instance
nc = Netcat('127.0.0.1', 53121)

# get to the prompt
nc.read_until('>')

# start a new note
nc.write('new' + '\n')
nc.read_until('>')

# set note 0 with the payload
nc.write('set' + '\n')
nc.read_until('id:')
