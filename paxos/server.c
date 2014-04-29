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
    int connfd;
    char buff [1024];

    struct sockaddr_in serv_addr;

    // create socket
    if (sockfd = socket (AF_INET, SOCK_STREAM, 0) < 0){
	printf ("\n Error creating socket\n");
	exit (1);
    }

    memset (&serv_addr, '0', sizeof (serv_addr));

    // setting addresses and port
    serv_addr.sin_family = AF_INET;
    serv_addr.sin_addr.s_addr = htonl (INADDR_ANY);
    serv_addr.sin_port = htons (8001);

/*    if (inet_pton (AF_INET, "127.0.0.1", &serv_addr.sin_addr) <= 0){
	printf ("\n Error creating IP\n");
	exit (1);
	}*/

    // bind and listen
    if (bind (sockfd, (struct sockaddr *)&serv_addr, sizeof (serv_addr)) < 0){
	printf ("Can't bind\n");
	close (sockfd);
	exit (1);
    }

    if (listen (sockfd, 10) < 0){
	printf ("\nDeaf. Can't listen\n");
	exit (1);
    }
    
    printf ("listening\n");

    // read from socket
    connfd = accept (sockfd, NULL, NULL);

    snprintf (buff, sizeof (buff), "Hello world!\n");

    write (connfd, buff, strlen (buff));

    close (connfd);
    close (sockfd);
    return 0;
}
