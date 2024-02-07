#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netinet/tcp.h>
#include <time.h>
#include <arpa/inet.h>
#include <limits.h>

#define CMD_Flag 0x8787

struct Command
{
    __uint32_t cmd;
    u_char token[32];
    u_char args[128];
};

struct Response
{
    __uint32_t code;
    u_char res[256];
};

// char *Token;

int main()
{
    int fd = socket(AF_INET, SOCK_STREAM, 0);

    struct sockaddr_in info;
    bzero(&info, sizeof(info));
    info.sin_family = PF_INET;
    info.sin_addr.s_addr = inet_addr("127.0.0.1");
    info.sin_port = htons(8765);

    connect(fd, (struct sockaddr *)&info, sizeof(info));

    struct Command cmd;
    memset(&cmd, 0, sizeof(cmd));
    cmd.cmd = CMD_Flag;
    write(fd, &cmd, sizeof(cmd));

    struct Response res;
    memset(&res, 0, sizeof(res));
    read(fd, &res, sizeof(res));

    write(1, &res, sizeof(res));

    return 0;
}
