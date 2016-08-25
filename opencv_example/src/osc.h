#ifndef __OSC_H__
#define __OSC_H__
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

#include "lo/lo.h"

#define M0(func, ...) func(__VA_ARGS__)
#define M1(func,args,...) M0(func, __VA_ARGS__, args[0])
#define M2(func,args,...) M1(func, args, __VA_ARGS__, args[1])
#define M3(func,args,...) M2(func, args, __VA_ARGS__, args[2])
#define M4(func,args,...) M3(func, args, __VA_ARGS__, args[3])
#define M5(func,args,...) M4(func, args, __VA_ARGS__, args[4])
#define M6(func,args,...) M5(func, args, __VA_ARGS__, args[5])
#define M7(func,args,...) M6(func, args, __VA_ARGS__, args[6])
#define M8(func,args,...) M7(func, args, __VA_ARGS__, args[7])
#define M9(func,args,...) M8(func, args, __VA_ARGS__, args[8])
#define M10(func,args,...) M9(func, args, __VA_ARGS__, args[9])
#define M11(func,args,...) M10(func, args, __VA_ARGS__, args[10])
#define M12(func,args,...) M11(func, args, __VA_ARGS__, args[11])
#define M13(func,args,...) M12(func, args, __VA_ARGS__, args[12])
#define M14(func,args,...) M13(func, args, __VA_ARGS__, args[13])
#define M15(func,args,...) M14(func, args, __VA_ARGS__, args[14])
#define M16(func,args,...) M15(func, args, __VA_ARGS__, args[15])

#define MN(n, func, args,...) switch(n) \
    { case 1: M1(func, args, __VA_ARGS__); break; \
      case 2: M2(func, args, __VA_ARGS__); break; \
      case 3: M3(func, args, __VA_ARGS__); break; \
      case 4: M4(func, args, __VA_ARGS__); break; \
      case 5: M5(func, args, __VA_ARGS__); break; \
      case 6: M6(func, args, __VA_ARGS__); break; \
      case 7: M7(func, args, __VA_ARGS__); break; \
      case 8: M8(func, args, __VA_ARGS__); break; \
      case 9: M9(func, args, __VA_ARGS__); break; \
      case 10: M10(func, args, __VA_ARGS__); break; \
      case 11: M11(func, args, __VA_ARGS__); break; \
      case 12: M12(func, args, __VA_ARGS__); break; \
      case 13: M13(func, args, __VA_ARGS__); break; \
      case 14: M14(func, args, __VA_ARGS__); break; \
      case 15: M15(func, args, __VA_ARGS__); break; \
      case 16: M16(func, args, __VA_ARGS__); break; \
    }

void init_connection(char *ip, char *port);
void send_msg(int argc, int argv[]);

#endif /* ifndef __OSC_H__ */
