#!/usr/bin/python3

from gevent import socket
from time import *

s = socket.socket ()

host = socket.gethostname ()
port = 8080

s.connect ((host, port))

s.settimeout (4)

sleep (6)

recv = s.recv (1024)

recv = recv.decode ('utf-8')

print (recv)

s.close()
