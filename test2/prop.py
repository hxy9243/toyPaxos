#!/usr/bin/python

import sys
sys.path.append ('..')
import time

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


    for c in cmds:
        t1 = time.time ()
        p.establish ()
        p.propose (c)
        t2 = time.time () 

        print ('starting at %f and end at %f' %(t1, t2))

if (__name__ == "__main__"):
    
    main (sys.argv)
