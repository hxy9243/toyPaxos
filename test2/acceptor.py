#!/usr/bin/python

import sys
sys.path.append ('..')

from paxos import acceptor
from paxos import config

import json


def main (argv):
    
    c = config.Config('_config').config[0]['quorum']

    a = acceptor.Acceptor (c[int (argv[1]) ])

    a.establish ()
    a.accept ()


if __name__ == '__main__':
    main (sys.argv)
