#include "my.h"
#include<string.h>

void liv7(u_int len,const u_char *p) {
  int i;
  if((int)len<=0) return;
  colore(5);
  printf("APPL |");
  for(i=1;i<=len;i++) {
    if(isprint(*p))
      printf("%c",*p);
    else
      printf(".");
    if(isascii(*p))
      fprintf(mem,"%c",*p);
    else
      fprintf(mem,".");
    p++;
    if((i%70)==0)
      printf("\n     |");
  }
  printf("\n");
  fflush(mem);
  decoded=1;
}
