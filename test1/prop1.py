#!/usr/bin/python

import sys
sys.path.append ('..')

from paxos import acceptor
from paxos import proposer
import json


config = {}
config['ID'] = 41000
config['type'] = 'proposer'

# quorum
quorum = {1: {'host':'127.0.0.1', 'port':8001},
          2: {'host':'127.0.0.1', 'port':8002}}


config['quorum'] = quorum
config['host'] = '127.0.0.1'
config['port'] = 8001

p = proposer.Proposer (config)

p.establish ()

p.propose ('You are a bitch')
