#!/usr/bin/python3

from gevent import socket
import time
import json

class Acceptor ():
    ''' Acceptor class for paxos acceptors '''

    def __init__ (self, config):
        ''' init acceptor '''
        # set state
        self.is_timedout = 0

        # set variable
        self.ID = config.ID
        self.purpose_num = 0
        self.quorum = config.quorum
        self.purposer_fd = {} # mapping ID to socket fd

        # create listener socket
        self.listener = socket.socket (socket.AF_INET, socket.SOCK_STREAM)


    def __del__ (self):
        ''' destructor for acceptor'''

        # delete socket
        self.listener.close ()
        for i in purposer_fd:
            if (purposer_fd[i] > 0):
                purposer_fd[i].close ()


    def log (self):
        ''' commit to log'''



    def establish (self):
        ''' establish bind and listen to the purposers '''
        host = self.quorum[self.ID]['host']
        port = self.quorum[self.ID]['port']

        # bind and listen to socket
        self.listener.settimeout (4)
        try:
            self.listener.bind ((address, port))
            self.listener.listen (10)
        except:
            print 'Fail to listen to port, exiting..'
            exit ()


    def accept (self):
        ''' keep accepting incoming requests '''
        while True:
            # keep accepting new requests
            try:
                c, addr = self.listener.accept ()
            except:
                print 'Error while accepting. Exiting..'
                exit ()

            # recv from accepted requests
            try:
                c.settimeout (4)
                msg = c.recv (2048)
                parse_msg (msg)
            except socket.timeout:
                print 'Timeout reached recieving.'
                pass
    

    def parse_msg (self, msg):
        ''' parse the msg from purposer '''
        # if a prepare
        

        # if a promise


    def accept (self, purposer_fd):
        ''' accept the purpose from purposer'''
        try:
            purposer_fd.recv (2048)
        except:
            print 'Error accepting from purposer'
        finally:
            purposer_fd.close ()


    def promise (self, purposer_fd):
        ''' promise the purposer 
        param: the purposer connection socket '''
        # prepare the promise msg


        # send the promise to purposer
        try:
            purposer_fd.send (msg)
        except:
            print 'Error sending promise msg'
            pass

        
