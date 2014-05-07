#!/usr/bin/python

import sys
sys.path.append ('..')

from paxos.config import Config


# quorum
quorum = [{'ID':1, 'host':'127.0.0.1', 'port':8001},
          {'ID':2, 'host':'127.0.0.1', 'port':8002}]

# proposer 1
config1 = {}
config1['ID'] = 41000
config1['type'] = 'proposer'
config1['propose_num'] = 41000
config1['quorum'] = quorum


# proposer 2
config2 = {}
config2['ID'] = 41001
config2['type'] = 'proposer'
config2['propose_num'] = 41001
config2['quorum'] = quorum


config = [config1, config2]

Config().dump (config, '_config')
