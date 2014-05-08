#!/usr/bin/python

import sys
sys.path.append ('..')

from paxos.config import Config


# quorum
quorum = [{'ID':1, 'host':'127.0.0.1', 'port':8001},
          {'ID':2, 'host':'127.0.0.1', 'port':8002}]

config = []
config1 = {}

for i in range (0, 32):
    config1 = {}
    config1['ID'] = i
    config1['type'] = 'proposer'
    config1['propose_num'] = 1000 + 32 * i
    config1['quorum'] = quorum
    
    config.append (config1)


Config().dump (config, '_config2')
