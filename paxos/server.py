#!/usr/bin/python3

from gevent import socket

s = socket.socket ()

host = socket.gethostname ()
port = 8002

s.bind ((host, port))

s.listen (5)

s.settimeout (4)



while True:
    while True:
        try:
            c, addr = s.accept()
            break
        except socket.timeout:
            print 'timeout'
            pass

        try:
            c.settimeout (4)
            c.sendall('fuck you')
            
        except socket.timeout:
            print 'timeout sending'
            break


c.close ()
