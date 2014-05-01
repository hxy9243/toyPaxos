/* toyPaxos Implementation
 * 
 * filename: proposer.c
 * description: Functions for proposers, 
 * implementation of the basic Paxos algorithm
 *
 */

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <errno.h>
#include <string.h>
#include <time.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <time.h>

#include "proposer.h"
#include "acceptor.h"


// init proposer
propose_t
init_proposer (int propose_num, int port_num, quorum_t quorum){


}

// propose a prepare message
int
propose_prepare (propose_t proposer){




}


// accept promise 
int
accept_promise (  ){



}



// time out
int
time_out ( ){



    
}

// free the proposer
int
free_proposer (  ){



}


