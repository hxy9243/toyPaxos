#!/usr/bin/python

import sys
sys.path.append ('..')

from paxos import acceptor
from paxos import proposer
from paxos import config
import json


def main (argv):
    c = config.Config(argv[1])

    p = proposer.Proposer (c.config[int(argv[2])])

    cmds = ['INSERT INTO FINAL_GRADE%s \nVALUE (\'xhu9\', \'A\');\n' % argv[2],
            'INSERT INTO TABLE%s\nVALUE(A, B, C, D, E);\n' % argv[2],
            'DELETE FROM TABLE%s\nWHERE \'student_name\'==\'JohnDoe\';\n' %argv[2]]

    s = ''
    N = p.updateNum ()
    while (s != 'quit'):
        s = raw_input ()
        
        p.establish ()
        p.propose (s)
        N = N + 32
        p.updateNum (N)


if (__name__ == "__main__"):
    
    main (sys.argv)
