#!/usr/bin/python

import sys
sys.path.append ('..')

from paxos import acceptor
import json


config = {}
config['ID'] = 1
config['type'] = 'purposer'

# quorum
quorum = {1: {'host':'127.0.0.1', 'port':8001},
          2: {'host':'127.0.0.1', 'port':8002}}

config['quorum'] = quorum
config['host'] = '127.0.0.1'
config['port'] = 8001


a = acceptor.Acceptor (config)


a.establish ()
a.accept ()
