/* toyPaxos Implementation
 * 
 * filename: socket.c
 * description: Socket I/O functions for the
 * communication between different processes
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


int
main (int argc, char** argv){
    
    int sockfd;
    char buff [1024];

    struct sockaddr_in serv_addr;

    // create socket
    if (sockfd = socket (AF_INET, SOCK_STREAM, 0) < 0){
	printf ("\n Error creating socket\n");
	exit (1);
    }

    // setting addresses and port
    memset (&serv_addr, '0', sizeof (serv_addr));
    
    serv_addr.sin_family = AF_INET;
    serv_addr.sin_port = htons (8001);

    if (inet_pton (AF_INET, "127.0.0.1", &serv_addr.sin_addr) <= 0){
	printf ("\n Error creating IP\n");
	exit (1);
    }

    // connect
    if (connect (sockfd, (struct sockaddr *)&serv_addr, sizeof (serv_addr)) < 0){
	printf ("\n Error connecting\n");
	exit (1);
    }

    // read from socket
    while ( read (sockfd, buff, sizeof (buff)) < 0){

	puts (buff);

    }

    return 0;
}
