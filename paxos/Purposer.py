#!/usr/bin/python

import gevent
from gevent import socket

class Purposer ():
    ''' A class of paxos purposers '''
    
    def __init__ (self, config):
        ''' init purposer '''
        # set state
        self.is_purpose = 0
        self.is_timedout = 0
        
        # set variable
        self.ID = config.ID
        self.value = config.ID
        self.purpose_num = config.ID
        self.quorum = config.quorum
        self.acceptors_fd = {}

        # create socket
        for i in self.quorum:
            s = socket.socket (socket.AF_INET, socket.SOCK_STREAM)
            self.acceptors_fd[i] = s


    def __del__ (self):
        ''' destructor for class '''
        # delete all acceptors
        for i in self.acceptors_fd:
            s = self.acceptors_fd[i]
            s.close ()


    def establish (self):
        ''' establish connections with acceptors'''
        # establish connection, connect to all acceptors
        try:
            for i in self.quorum:
                address = self.quorum[i]['address']
                port = self.quorum[i]['port']
                s = self.acceptors_fd[i]

                s.settimeout (5)
                s.connect ((address, port))
                
        except:
            print ("Problem connecting to addresses")
            exit ()


    def send_quorum (self, msg):
        ''' Send msg to all the quorum'''
        try:
            for i in self.quorum:
                s = self.acceptors_fd[i]
                s.sendall (msg)
        # raise timeout Exception
        except socket.timeout:
            raise socket.timeout
        except:
            print 'Unknown error while sending'
            exit ()


    def recv_quorum (self):
        ''' Recv from the quorum '''
        try:
            for i in self.quorum:
                s = self.acceptors_fd[i]
                msg = s.recv (2048)
                parse_msg (msg)

        # raise timeout Exception
        except socket.timeout:
            raise socket.timeout
        except:
            print 'Unknown error while recving'
            exit ()


    def prepare (self):
        ''' purpose a value'''
        # prepare the prepare msg
        prepare_msg = ''

        # send accept signals to all acceptors
        try:
            self.send_quorum (prepare_msg)
        except:
            # handle prepare failure
            self.prepare_except ()


    def accept (self):
        ''' send the accept value to all acceptors '''
        accept_msg = ''

        try:
            self.send_quorum (accept_msg)
        except:
            # TODO: handle accept excepts
            pass


    def purpose_except (self):
        pass



