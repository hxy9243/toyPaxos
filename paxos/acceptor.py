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
        self.ID = config['ID']
        self.propose_num = -1
        self.promise_ID = -1
        self.quorum = config['quorum']
        self.proposer_fd = {} # mapping ID to socket fd
        self.value = ''
        self.lock = 'unlock'


    def __del__ (self):
        ''' destructor for acceptor'''

        # delete socket
        self.listener.close ()
        for i in self.proposer_fd:
            if (self.proposer_fd[i] > 0):
                self.proposer_fd[i].close ()


    def log (self):
        ''' commit to log'''
        # TODO: commit to log
        # clear self value
        print self.value
        self.value = ''


    def establish (self):
        ''' establish bind and listen to the proposers '''
        # create listener socket
        self.listener = socket.socket (socket.AF_INET, socket.SOCK_STREAM)
        print (self.listener)

        host = self.quorum[self.ID]['host']
        port = self.quorum[self.ID]['port']

        # bind and listen to socket
        self.listener.bind ((host, port))
        self.listener.listen (10)


    def gen_msg (self, msg_type):
        ''' generate return msg to proposer'''
        # Msg type:
        # 'promise': promise a propose
        # 'NACK': I don't accept
        msg = {}
        msg['ID'] = self.ID
        msg['msg_type'] = msg_type

        return json.dumps (msg)


    def parse_msg (self, msg):
        ''' parse the msg from proposer '''
        print ('parsing msg')
        print msg
        try:
            msg = json.loads (msg)
        except:
            print 'Unknown msg'
            return ('unknown msg', msg)

        print ('accepting msg type %s' % msg['msg_type'])
        print ('accepting propose number %d' % msg['propose_num'])
        print ('self propose number %d' % self.propose_num)

        if (msg['msg_type'] == 'prepare'):
            # if propose number higher
            if (msg['propose_num'] > self.propose_num):
                # prepare number 
                self.propose_num = msg['propose_num']
                self.promise_ID = msg['ID']
                return ('promise', msg)
            else:
                return ('NACK', msg)

        elif (msg['msg_type'] == 'accept'):
            if (msg['ID'] == self.promise_ID):
                self.promise_ID = -1
                return ('accept', msg)


    def send (self, proposer_fd, msg_type):
        ''' promise the proposer 
        param: the proposer connection socket '''
        # prepare the promise msg
        msg = self.gen_msg (msg_type)

        print msg

        # send the promise to proposer
        try:
            proposer_fd.send (msg)
        except:
            print 'Error sending msg'
            pass
        

    def accept (self):
        ''' keep accepting incoming requests '''
        while True:
            # keep accepting new requests
            try:
                c, addr = self.listener.accept ()
                print c
                print addr
                print ('[log] accepting from address %s' % (addr[0]))
            except Exception as p:
                print 'Error while accepting. Exiting..'
                print p
                exit ()

            # recv from accepted requests
            try:
#                c.settimeout (4)
                msg = c.recv (2048)
                msg_type, msg = self.parse_msg (msg)

                if (msg_type == 'promise'):
                    # promise a propose
                    self.send (c, 'promise')
                    
                    print ('[log] promised proposer ID %d' % msg['ID'])

                    msg = c.recv (2048)
                    msg_type, msg = self.parse_msg (msg)

                    if (msg_type == 'accept'):

                        self.value = msg['value']
                        print ('logging')
                        self.log ()
                        c.close ()
                        continue

                else: # a stale request
                    self.send (c, 'NACK')
                    print ('NACK. Ignoring propose')
                    c.close ()
                    continue

            except socket.timeout:
                print 'Timeout reached receiving.'
                continue
            
            except Exception as p:
                print 'Unknown error when accepting connections'
                print p
                exit ()
    
