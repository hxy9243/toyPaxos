#!/usr/bin/python

import socket
import gevent
from gevent import socket

class Purposer ():
    ''' A class of paxos purposers '''
    
    def __init__ (self, config):
        ''' init purposer '''
        # set state
        is_purpose = 0
        is_timedout = 0
        
        # set variable
        purpose_num = config.ID
        quorum = config.quorum
        acceptors = {}

        # create socket and bind to address
        port = config.port
        address = config.address

        skt = socket.socket (socket.AF_INET, socket.SOCK_STREAM)
        try:
            skt.bind ((address, port))
        except:
            print ("Problem binding to address")
            exit ()


    def __del__ (self):
        ''' destructor for class '''
        self.skt.close ()


    def establish (self):
        # establish connection, accept from all acceptors
        


    def prepare (self):
        ''' purpose a value'''
        # send accept signals to all acceptors
        
        # raise timeout Exception


    def accept (self):
        ''' accept '''
        pass

    def purpose (self):
        pass




