#!/usr/bin/python

from gevent import socket
import time
import json

class Purposer ():
    ''' Purposer class for paxos purposers '''
    
    def __init__ (self, config):
        ''' init purposer '''
        # set state
        
        self.retry_count = 3
        
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


    def set_val (self, val):
        ''' set the value of the purpose '''
        self.value = val


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
                print 'Connection to acceptors established.'
                
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
                msg_list.append (s.recv (2048))

            # parse all the recieved msg
            return self.parse_msg (msg_list)

        # raise timeout Exception
        except socket.timeout:
            raise socket.timeout
        except:
            print 'Unknown error while recving'
            exit ()


    def parse_msg (self, m_list):
        ''' Parse incoming messages from acceptor after prepare
            param: list of all msg '''
        msg_list = []

        for m in msg_list:
            msg_list.append (json.loads (m))
        
        if (m['type'] == 'promise' for all m in msg_list):
            return 'promise'

        else:
            return 'NACK'

    
    def updateNum (self):

        # to guarantee no collision between purposers,
        # TODO: a more sophiscated way?
        self.purpose_num = self.purpose_num + 32


    def gen_msg (self, msg_type, value = ''):
        ''' return the prepare message to send to acceptors '''
        # Msg type:
        # 'prepare': inform acceptors to prepare for a purpose
        # 'accept': inform acceptors to accept for a purpose

        Msg = {}
        Msg['ID'] = self.ID
        Msg['msg_type'] = msg_type
        Msg['prepare_num'] = self.prepare_num
        Msg['value'] = value
        return json.dumps (Msg)


    def send_prepare (self):
        ''' purpose for a purpose number'''

        # send prepare signals to all acceptors
        try:
            self.send_quorum (self.gen_msg ('prepare'))
        except socket.timeout:
            # handle prepare failure
            raise socket.timeout
        except:
            print 'Unkown exception in preparing. Exiting..'
            exit ()


    def send_accept (self):
        ''' send the accept value to all acceptors '''

        try:
            self.send_quorum (self.gen_msg ('accept', self.value))
        except socket.timeout:
            raise socket.timeout
        except:
            print 'Unknown exception in sending accepting. Exiting...'
            exit ()
        

    def purpose_except (self):
        ''' An exception inside the purposer, try to handle it'''
        self.updateNum ()

        # update retry
        self.retry_count = self.retry_count - 1
        if (self.retry_count == 0):
            print ('Purposer with ID: %d failed with purpose num %d'
                   % (self.ID, self.purpose_num))
            return 'fail'

        else:
            return 'retry'


    def purpose (self, value):
        ''' purpose a value to all acceptors'''
        # TODO: handle cases where value is too large (>2048)
        self.updateNum ()
        self.retry_count = 3
        self.value = value

        # send prepare to all acceptors
        while True:
            try:
                self.send_prepare ()
                if (self.recv_quorum () == 'promise'):
                    break
            except socket.timeout:
                if (self.purpose_except () == 'retry'):
                    continue
                else:
                    return 'fail'
            except:
                print ('Unknown erro while preparing')
                exit ()
                
        # accept
        try:
            self.send_accept ()
        except:
            print ('Error sending accept')
            return 'fail'
                
        # purpose successful, clean up
        print 'purpose successful'
        return 'success'
