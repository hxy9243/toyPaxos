#!/usr/bin/python

from gevent import socket
import time
import json

class Purposer ():
    ''' Purposer class for paxos purposers '''
    
    def __init__ (self, config):
        ''' init purposer '''
        # set state
        
        self.is_timedout = 0 # how many times timedout
        
        # set variable
        self.ID = config.ID
        self.value = ''
        self.purpose_num = config.ID
        self.quorum = config.quorum
        self.acceptors_fd = {} # mapping ID to socket fd

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


    def set_val (self, msg):
        ''' set the value of the purpose '''
        self.value = msg


    def establish (self):
        ''' Establish connections with acceptors '''
        # establish connection, connect to all acceptors
        try:
            for i in self.quorum:
                host = self.quorum[i]['host']
                port = self.quorum[i]['port']
                s = self.acceptors_fd[i]

                s.settimeout (5)
                s.connect ((host, port))
                
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
        msg_list = []
        try:
            for i in self.quorum:
                s = self.acceptors_fd[i]
                msg_list.append ( s.recv (2048))

            # parse all the recieved msg
            parse_msg (msg_list)

        # raise timeout Exception
        except socket.timeout:
            raise socket.timeout
        except:
            print 'Unknown error while recving'
            exit ()


    def parse_msg (self, msg_list):
        ''' Parse incoming messages from acceptor
            param: list of all msg '''
        
        pass


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
        ''' An exception inside the purposer, try to handle it'''
        # resend the purpose


        pass



