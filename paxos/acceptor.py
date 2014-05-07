#!/usr/bin/python

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
        self.purpose_num = -1
        self.promise_ID = -1
        self.quorum = config.quorum
        self.purposer_fd = {} # mapping ID to socket fd
        self.value = ''

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
        # TODO: commit to log
        # clear self value
        print self.value
        self.value = ''


    def establish (self):
        ''' establish bind and listen to the purposers '''
        host = self.quorum[self.ID]['host']
        port = self.quorum[self.ID]['port']

        # bind and listen to socket
        self.listener.bind ((address, port))
        self.listener.listen (10)


    def gen_msg (self, msg_type):
        ''' generate return msg to purposer'''
        # Msg type:
        # 'promise': promise a purpose
        # 'NACK': I don't accept
        msg = {}
        msg['ID'] = self.ID
        msg['msg_type'] = msg_type

        return json.dumps (msg)


    def parse_msg (self, msg):
        ''' parse the msg from purposer '''
        # if a prepare
        try:
            msg = json.loads (msg)
        except:
            print 'Unknown msg'
            return 'unknown msg'

        if (msg['msg_type'] == 'prepare'):
            # if purpose number higher
            if (msg['propose_num'] > self.propose_num):
                # prepare number 
                self.propose_num = msg['propose_num']
                self.promise_ID = msg['ID']
                return 'promise'
            else:
                return 'NACK'

        elif (msg['msg_type'] == 'accept'):
            if (msg['ID'] == self.promise_ID):
                self.promise_ID = -1
                return 'accept'


    def send (self, purposer_fd, msg_type):
        ''' promise the purposer 
        param: the purposer connection socket '''
        # prepare the promise msg
        msg = gen_msg (msg_type)

        # send the promise to purposer
        try:
            purposer_fd.send (msg)
        except:
            print 'Error sending promise msg'
            pass
        

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
                msg = self.parse_msg (msg)

                if (msg == 'prepare'):
                    self.send (c, 'promise')
                elif (msg == 'accept'):
                    self.value = msg.value
                    self.log ()
                else: # a stale request
                    self.send (c, 'NACK')
                    continue

            except socket.timeout:
                print 'Timeout reached recieving.'
                continue
            
            except:
                print 'Unknown error when accepting connections'
                exit ()
    
