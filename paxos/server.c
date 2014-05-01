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
#include <time.h>

int main(int argc, char *argv[])
{
  int listenfd = 0, connfd = 0;
  struct sockaddr_in serv_addr;

  char sendBuff[1025];
  time_t ticks;

  listenfd = socket(AF_INET, SOCK_STREAM, 0);
  memset(&serv_addr, '0', sizeof(serv_addr));
  memset(sendBuff, '0', sizeof(sendBuff));

  serv_addr.sin_family = AF_INET;
  serv_addr.sin_addr.s_addr = htonl(INADDR_ANY);
  serv_addr.sin_port = htons(5000);

  if (bind(listenfd, (struct sockaddr*)&serv_addr, sizeof(serv_addr)) < 0){
    perror ("Can't bind!\n");
    exit (1);
  }

  if (listen(listenfd, 10) < 0){
    perror ("Can't listen!\n");
    exit (1);
  }

  while(1)
    {
      connfd = accept(listenfd, (struct sockaddr*)NULL, NULL);

      ticks = time(NULL);
      snprintf(sendBuff, sizeof(sendBuff), "%.24s\r\n", ctime(&ticks));
      write(connfd, sendBuff, strlen(sendBuff));

      close(connfd);
      sleep(1);
    }
}
