#include "my.h"
#include<string.h>

void liv7(u_int len,const u_char *p) {
  int i = 1;
  if((int)len<=0) return;
  //increasing counter
  counter.lvl7++;
  int not_readable = 0;
  colore(5);
  myprintf("APPL |");
  for(i = 1; i <= len*2; i++) {
    if(isprint(*p)) {
      myprintf("%c", *p);
      not_readable = 0;
    } else {
      myprintf(".");
      not_readable++;
    }
    if(isascii(*p)) {
      fprintf(mem, "%c", *p);
      not_readable = 0;
    } else {
      fprintf(mem,".");
      not_readable++;
    }
    p++;
    if (not_readable > 100) break;
    if((i%70)==0)
      myprintf("\n     |");
  }
  myprintf("\n");
  fflush(mem);
  decoded=1;
}
