/* toyPaxos Implementation
 * 
 * filename: proposer.h
 * description: Functions for proposers, 
 * implementation of the basic Paxos algorithm
 *
 */


#ifndef __PROPOSER_H__
#define __PROPOSER_H__


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

// data structures

typedef struct proposer{
    
    int ID;
    int propose_num;
    int listenfd;
    int connectfd;
    int num_acceptors;
    quorum_t quorum;
    
}proposer_t;


// function declaration


int init_proposer ( );


int propose_prepare ( );


int time_out ( );


int free_proposer (  );


void paxos_log ( );


#endif
