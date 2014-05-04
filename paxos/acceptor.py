#!/usr/bin/python3

from gevent import socket
import time
import json

class Acceptor ():
    ''' Acceptor class for paxos acceptors '''

    def __init__ (self, config):
        ''' init acceptor '''
        # set state
        

        # set variable


        # create socket

    def __del__ (self):
        ''' destructor for acceptor'''

        # delete socket
        

    def log (self):
        ''' commit to log'''


    def establish (self):
        ''' establish connections to the purposers '''
        


    def accept (self):
        ''' keep accepting incoming requests '''


    

    def parse_msg (self, msg):
        ''' parse the msg from purposer '''


    def promise (self, purposer_fd):
        ''' promise the purposer 
        param: the purposer connection socket '''
        

        
