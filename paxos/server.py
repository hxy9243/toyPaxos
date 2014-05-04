#!/usr/bin/python3

from gevent import socket

s = socket.socket ()

host = socket.gethostname ()
port = 8080

s.bind ((host, port))

s.listen (5)

s.settimeout (4)



while True:
    while True:
        try:
            c, addr = s.accept()
            break
        except:
            print 'timeout'
            pass


    while True:
        try:
            c.sendall('fuck you')
            
        except:
            print 'timeout sending'
            break


c.close ()
