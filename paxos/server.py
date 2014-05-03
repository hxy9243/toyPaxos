#!/usr/bin/python3

import socket


s = socket.socket ()

host = socket.gethostname ()
port = 8080

s.bind ((host, port))

s.listen (5)

s.settimeout (4)

while True:
    try:
        c, addr = s.accept()

    except:
        print 'timeout'
        break;

    c.sendall ('Fuck you Paxos!'.encode ('utf-8'))
    c.close ()
