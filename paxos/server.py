#!/usr/bin/python3

import socket


s = socket.socket ()

host = socket.gethostname ()
port = 8080

s.bind ((host, port))

s.listen (5)

while True:
    c, addr = s.accept()

    c.sendall ('Fuck you Paxos!'.encode ('utf-8'))
    c.close ()
