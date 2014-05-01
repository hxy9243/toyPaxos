/* toyPaxos Implementation
 * 
 * filename: acceptor.h
 * description: Functions for acceptors, 
 * implementation of the basic Paxos algorithm
 *
 */

#ifndef __ACCEPTOR_H__
#define __ACCEPTOR_H__


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

// data structure

typedef struct acceptor{
    
    int ID;
    int propose_num;
    int listenfd;
    int connectfd;

}acceptor_t;

// function declaration

// init proposer
int init_acceptor ( );

// promise a proposer
int promise ( );

// accept promise 
int accept_promise (  );

// learn
int teach_learner ( );

// free the proposer
int free_acceptor (  );



#endif
