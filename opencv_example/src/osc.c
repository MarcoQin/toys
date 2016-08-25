#include "osc.h"

void handle_send_result(int rt, lo_address t) {
    if (rt == -1) {
        fprintf(stderr, "OSC error %d: %s\n", lo_address_errno(t), lo_address_errstr(t));
    }
}

lo_address addr;

void init_connection(char *ip, char *port) {
    /* addr = lo_address_new("127.0.0.1", "7770"); */
    addr = lo_address_new(ip, port);
}

void send_msg(int argc, int argv[]) {
    char type[argc+1];
    int i;
    for (i = 0; i < argc; i++) {
        type[i] = 'i';
    }
    type[i] = '\0';
    int end = argc - 1;
    int tmp;
    for (i = 0; i < argc/2; i++) {
        tmp = argv[i];
        argv[i] = argv[end];
        argv[end--] = tmp;
    }
    MN(argc, lo_send, argv, addr, "/test", type);
}

#ifdef __DEBUG
int main(int argc, char *argv[])
{
    init_connection("127.0.0.1", "7770");
    int args[] = {1, 2, 3, 4, 5, 6, 7, 8};
    send_msg(8, args);
    int args1[] = {0, 2, 3, 4, 0, 6, 7, 8};
    send_msg(8, args1);
    return 0;
}
#endif
