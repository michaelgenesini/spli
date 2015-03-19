#include "my.h"

void liv2(u_char *user,const struct pcap_pkthdr *h,const u_char *p) {
  
  int i;
  const u_char *mp;
  u_int len,type;
  char tratt[]="####################";
  
  unknown=0;
  filt_kill=0;
  decoded=0;
  olen=0;
  type=ntohs(*(u_int *)(p+12));
  len=h->len;
  //testing purpose, set p_live2 = true;
  if(p_liv2) {
    colore(2);
    myprintf("802.3|");//MODIFICATO myprintf
    print_liv2(p+6);
    myprintf(" -> ");//MODIFICATO myprintf
    print_liv2(p);
    myprintf(" Type:%04x Len:%d",type,len); //MODIFICATO myprintf
    myprintf("\n"); //MODIFICATO myprintf
  }
  //salgo al livello 3
  //printf("Sto per andare al livello 3, type %d\n", type);
  liv3(type,p+14);

  //provo a stampare outbuf
  printf("%s\n", outbuf);

  if(olen!=0) {
    o_colore(1);
    if(p_decoded&&decoded)
      printf("\n%s Decoded %s\n%s",tratt,tratt,outbuf);
    if(p_filt_kill&&filt_kill)
      printf("\n%s Filt_Kill %s\n%s",tratt,tratt,outbuf);
    if(p_unknown&&unknown)
      printf("\n%s Unknown %s\n%s",tratt,tratt,outbuf);
    fflush(stdout);
  }

}