#!/usr/bin/python3

import json

class Config ():
    ''' The config class for reading and parsing
    configurations for paxos library'''

    def __init__ (self, filename = None):
        ''' read from config file'''
        self.config = {}
        if (filename == None):
            self.default ()

        else:
            try:
                f = open ('config', 'r')
                self.config = json.load (f)
                f.close ()
            except:
                print 'opening file error, using default'
                self.default ()


    def default (self):
        ''' generating default value for config'''
        config = {}
        config['ID'] = 0
        config['type'] = 'purposer'
        # quorum
        quorum = [{'ID':1, 'host':'127.0.0.1', 'port':8001},
                  {'ID':2, 'host':'127.0.0.1', 'port':8002},
                  {'ID':3, 'host':'127.0.0.1', 'port':8003}]
        config['quorum'] = quorum

        self.config = config        


    def dumps (self, filename):
        ''' generate config file'''
        f = open (filename, 'w')
        json.dump (self.config, f)
        f.close ()
