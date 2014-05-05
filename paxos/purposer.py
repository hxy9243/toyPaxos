#!/usr/bin/python

from gevent import socket
import time
import json

class Purposer ():
    ''' Purposer class for paxos purposers '''
    
    def __init__ (self, config):
        ''' init purposer '''
        # set state
        
        self.is_timedout = 3 # how many times receive timedout
        
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
        # TODO: parse msg 
        if (m['type'] == 'promise' for all m in msg_list):
            return 'promise'

        else:
            return 'NACK'

    
    def updateNum (self):
        self.purpose_num = self.purpose_num + 32


    def gen_msg (self, msg_type, value = ''):
        ''' return the prepare message to send to acceptors '''
        Msg = {}
        Msg['ID'] = self.ID
        Msg['msg_type'] = msg_type
        Msg['value'] = value
        return json.dumps (Msg)


    def send_prepare (self):
        ''' purpose a value'''
        # TODO: prepare the prepare msg
        prepare_msg = self.gen_msg ('prepare')

        # send prepare signals to all acceptors
        try:
            self.send_quorum (prepare_msg)
        except socket.timeout:
            # handle prepare failure
            raise socket.timeout
        except:
            print 'Unkown exception in prepare signal. Exiting..'
            exit ()


    def send_accept (self):
        ''' send the accept value to all acceptors '''
        accept_msg = self.gen_msg ('accept', self.value)

        try:
            self.send_quorum (accept_msg)
        except:
            # TODO: handle accept excepts
            return 'Error'
        
        # update the purpose number
        self.updateNum ()
        return 'Success'
        

    def purpose_except (self):
        ''' An exception inside the purposer, try to handle it'''
        # resend the purpose
        self.retry_count = self.retry_count - 1
        if (self.retry_count == 0):
            print ('Purposer with ID: %d failed with purpose num %d'
                   % (self.ID, self.purpose_num))

        self.updateNum ()


    def purpose (self, value):
        ''' purpose a value to all acceptors'''
        self.value = value

        # send prepare to all acceptors
        while (self.retry_count != 0):
            try:
                self.send_prepare ()
                break
            except socket.timeout:
                self.purpose_except ()
            except:
                print 'Unknown error while preparing'
                exit ()

        # send accept msg to all acceptors
        while (self.retry_count != 0):
            try:
                self.send_accept ()
                break
            except socket.timeout:
                self.purpose_except ()
            except:
                print 'Unknown error while preparing'
                exit ()
                
        print 'purpose successful'
