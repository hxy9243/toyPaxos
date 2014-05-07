#!/usr/bin/python

from gevent import socket
import time
import json

class Proposer ():
    ''' Proposer class for paxos proposers '''
    
    def __init__ (self, config):
        ''' init proposer '''
        # set state
        
        self.retry_count = 3
        
        # set variable
        self.ID = config['ID']
        self.value = ''
        self.propose_num = config['ID']
        self.quorum = config['quorum']
        self.acceptors_fd = {} # mapping ID to socket fd


    def __del__ (self):
        ''' destructor for class '''
        self.close_all ()


    def close_all (self):
        # delete all acceptors
        for i in self.acceptors_fd:
            s = self.acceptors_fd[i]
            s.close ()


    def set_val (self, val):
        ''' set the value of the propose '''
        self.value = val


    def establish (self):
        ''' Establish connections with acceptors '''
        # create socket
        for i in self.quorum:
            s = socket.socket (socket.AF_INET, socket.SOCK_STREAM)
            self.acceptors_fd[i] = s

        # establish connection, connect to all acceptors
        try:
            for i in self.quorum:
                host = self.quorum[i]['host']
                port = self.quorum[i]['port']
                s = self.acceptors_fd[i]

                s.settimeout (5)
                s.connect ((host, port))
                print 'Connection to acceptors established.'
                
        except Exception as e:
            print e
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
        except Exception as e:
            print (e)
            print 'Unknown error while sending'
            exit ()


    def recv_quorum (self):
        ''' Recv from the quorum '''
        msg_list = []
        try:
            for i in self.quorum:
                s = self.acceptors_fd[i]
                msg_list.append (s.recv (2048))

            # parse all the recieved msg
            return self.parse_msg (msg_list)

        # raise timeout Exception
        except socket.timeout:
            raise socket.timeout
        except:
            print 'Unknown error while recving'
            exit ()


    def updateNum (self):

        # to guarantee no collision between proposers,
        # TODO: a more sophiscated way?
        self.propose_num = self.propose_num + 32


    def gen_msg (self, msg_type, value = ''):
        ''' return the prepare message to send to acceptors '''
        # Msg type:
        # 'prepare': inform acceptors to prepare for a propose
        # 'accept': inform acceptors to accept for a propose

        Msg = {}
        Msg['ID'] = self.ID
        Msg['msg_type'] = msg_type
        Msg['propose_num'] = self.propose_num
        Msg['value'] = value
        m = json.dumps (Msg)
        print m
        return m


    def parse_msg (self, m_list):
        ''' Parse incoming messages from acceptor after prepare
            param: list of all msg '''
        # TODO: handle exceptions as duplicate from acceptors

        msg_list = []

        print m_list

        try:
            for m in m_list:
                msg_list.append (json.loads (m))

        except Exception as p:
            print 'Error parsing received msg'
            print p
            return 'NACK'
        

        if ( all (m['msg_type'] == 'promise' for m in msg_list) ):
            return 'promise'

        else:
            return 'NACK'

    
    def send_prepare (self):
        ''' prepare for a propose number'''

        # send prepare signals to all acceptors
        try:
            print ('sending prepare')
            self.send_quorum (self.gen_msg ('prepare'))
        except socket.timeout:
            # handle prepare failure
            raise socket.timeout
        except Exception as e:
            print 'Unkown exception in preparing. Exiting..'
            print (e)
            exit ()


    def send_accept (self):
        ''' send the accept value to all acceptors '''

        try:
            self.send_quorum (self.gen_msg (msg_type='accept', value= self.value))
        except socket.timeout:
            raise socket.timeout
        except:
            print 'Unknown exception in sending accepting. Exiting...'
            exit ()
        

    def propose_except (self):
        ''' An exception inside the proposer, try to handle it'''

        # update retry
        self.retry_count = self.retry_count - 1
        print self.retry_count
        if (self.retry_count <= 0):
            print ('Proposer with ID: %d failed with propose num %d'
                   % (self.ID, self.propose_num))
            return 'fail'

        else:
            self.updateNum ()
            return 'retry'


    def propose (self, value):
        ''' propose a value to all acceptors'''
        # TODO: handle cases where value is too large (>2048)
        self.updateNum ()
        self.value = value

        # send prepare to all acceptors
        while True:
            try:
                self.send_prepare ()
                if (self.recv_quorum () == 'promise'):
                    print ('accept promise from acceptor')
                    break
                else:
                    if (self.propose_except () == 'retry'):
                        self.close_all ()
                        self.establish ()
                        self.propose (self.value)
                        return

            except socket.timeout:
                if (self.propose_except () == 'retry'):
                    self.close_all ()
                    self.establish ()
                    self.propose (self.value)
                else:
                    return 'fail'
            except Exception as e:
                print e
                print ('Unknown error while preparing')
                exit ()
                
        # accept
        try:
            print ('sending accept')
            self.send_accept ()
        except:
            print ('Error sending accept')
            return 'fail'
                
        # propose successful, clean up
        print 'propose successful'
        self.updateNum ()
        self.retry_count = 3
        self.close_all ()
        return 'success'
