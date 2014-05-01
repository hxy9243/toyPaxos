/* toyPaxos Implementation
 * 
 * filename: paxosSocket.c
 * description: The socket send/accept interface
 * for the protocol
 *
 */

#include <sys/socket.h>
#include <sys/types.h>
#include <netinet/in.h>
#include <netdb.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>
#include <errno.h>
#include <arpa/inet.h>

// init the socket 
// param: port_num
// return: listenfd
int init_listen (int port_num){
    int listenfd = 0;
    struct sockaddr_in serv_addr;

    listenfd = socket (AF_INET, SOCK_STREAM, 0);
    memset (&serv_addr, '0', sizeof (serv_addr));
    // memset (sendBuff, '0', sizeof (sendBuff));

    // set server address
    serv_addr.sin_family = AF_INET;
    serv_addr.sin_addr.s_addr = htonl (INADDR_ANY);
    serv_addr.sin_port = htons (port_num);

    // bind and listen
    if (bind(listenfd, (struct sockaddr*)&serv_addr, sizeof(serv_addr)) < 0){
	perror ("Can't bind!\n");
	return -1;
    }

    return listenfd;
}

// init the connect socket
// param: port_num, ip
// return: socketfd
int init_connect (int port_num, char *ip){
    int sockfd = 0;
    struct sockaddr_in serv_addr;

    if((sockfd = socket(AF_INET, SOCK_STREAM, 0)) < 0){
	perror ("Could not create socket \n");
	return -1;
    }

    memset(&serv_addr, '0', sizeof(serv_addr));

    serv_addr.sin_family = AF_INET;
    serv_addr.sin_port = htons (port_num);

    if (inet_pton (AF_INET, ip, &serv_addr.sin_addr) <= 0){
	perror ("inet_pton error occurred\n");
	return -1;
    }

    return sockfd;
}

// start listen the socket
// param: listenfd
// return: errno
int socket_listen (int listenfd, int listen_num ){
    return listen (listenfd, listen_num);
}

int connect_socket (  ){



}

// behaviors on accept 
// 
int on_accept (  ){


}

// read from the socket
int paxos_read (   ){


}

// write to the socket
int paxos_write (  ){




}
