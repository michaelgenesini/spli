#include "my.h"

void liv3(u_int type,const u_char *p) {
  const u_char *mp;
  int i,j,k,r,ihl,flag;
  u_int id,fragm,len;
  u_char ttl,proto;
  u_long flow;
  struct filt_ipv4 *aux_ipv4;
  struct filt_ipv6 *aux_ipv6;
  int mask[8]={0,0x80,0xc0,0xe0,0xf0,0xf8,0xfc,0xfe};
  
  switch(type) {
    // IPv4
    case 0x800:
      if(!r_ipv4)
        return;    
      flag=0;
      for(aux_ipv4=filt_ipv4;aux_ipv4!=NULL;aux_ipv4=aux_ipv4->next) {
        i=aux_ipv4->scid;
        j=i/8;
        r=i%8;
        mp=p+12;
        for(k=0;k<j;k++)
          if(*(mp+k)!=aux_ipv4->sip[k])
            break;
        if(k!=j||((*(mp+j))&mask[r])!=(aux_ipv4->sip[j]&mask[r])) {
          flag=1;
          continue;
        }
        i=aux_ipv4->dcid;
        j=i/8;
        r=i%8;
        mp=p+16;
        for(k=0;k<j;k++)
          if(*(mp+k)!=aux_ipv4->dip[k])
            break;
        if(k!=j||((*(mp+j))&mask[r])!=(aux_ipv4->dip[j]&mask[r])) {
          flag=1;
          continue;
        }
        flag=0;
        break;
      }
      id=ntohs(*(u_int *)(p+4));
      ttl=*(p+8);
      proto=*(p+9);
      len=ntohs(*(u_int *)(p+2));
      ihl=((*p)&0x0f)*4;
      fragm=ntohs(*(u_int *)(p+6));
      if(p_ipv4) {
        colore(3);
        printf("IPv4 |");
        print_ipv4(p+12);
        printf(" -> ");
        print_ipv4(p+16);
        printf(" Id:%d Ttl:%d Proto:%d Len:%d",id,ttl,proto,len);
        if(fragm&0x4000)
          printf(" DF");
        printf(" Fragm:%d%c\n",fragm&0x1fff,(fragm&0x2000)?'M':'F');
      }
      if(flag) {
        filt_kill=1;
        return;
      }
      liv4(proto,len-ihl,p+ihl);
      return;
    // IP v6
    case 0x86dd:
      if(!r_ipv6)
        return;    
      flag=0;
      for(aux_ipv6=filt_ipv6;aux_ipv6!=NULL;aux_ipv6=aux_ipv6->next) {
        i=aux_ipv6->scid;
        j=i/8;
        r=i%8;
        mp=p+8;
        for(k=0;k<j;k++)
          if(*(mp+k)!=aux_ipv6->sip[k])
            break;
        if(k!=j||((*(mp+j))&mask[r])!=(aux_ipv6->sip[j]&mask[r])) {
          flag=1;
          continue;
        }
        i=aux_ipv6->dcid;
        j=i/8;
        r=i%8;
        mp=p+24;
        for(k=0;k<j;k++)
          if(*(mp+k)!=aux_ipv6->dip[k])
            break;
        if(k!=j||((*(mp+j))&mask[r])!=(aux_ipv6->dip[j]&mask[r])) {
          flag=1;
          continue;
        }
        flag=0;
        break;
      }
      ttl=*(p+7);
      proto=*(p+6);
      flow=ntohl(*(u_long *)(p))&0x00ffffff;
      len=ntohs(*(u_int *)(p+4));
      if(p_ipv6) {
        colore(3);
        printf("IPv6 |");
        print_ipv6(p+8);
        printf(" -> ");
        print_ipv6(p+24);
        printf(" Proto:%d Hop:%d Len:%d Flow:%ld\n",proto,ttl,len,flow);
      }
      if(flag) {
        filt_kill=1;
        return;
      }
      liv4(proto,len-40,p+40);
      return;

    case 0x0806:
      if(!p_arp) return;
      colore(3);
      printf("ARP  |");
      switch(htons(*(u_int *)(p+6))) {
        case 1:
          printf("Request   ");
          break;
        case 2:
          printf("Reply     ");
          break;
        case 3:
          printf("R_Request ");
          break;
        case 4:
          printf("R_Reply   ");
          break;
      }
      printf(" ");
      print_liv2(p+8);
      printf(" -> ");
      print_liv2(p+18);
      printf(" ");
      print_ipv4(p+14);
      printf(" -> ");
      print_ipv4(p+24);
      printf("\n");
      decoded=1;
      return;

    default:
      unknown=1;
      return;
    }
}