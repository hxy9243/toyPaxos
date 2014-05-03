#!/usr/bin/python3

import socket

s = socket.socket ()

host = socket.gethostname ()
port = 8080

s.connect ((host, port))

recv = s.recv (1024)

recv = recv.decode ('utf-8')

print (recv)

s.close()
