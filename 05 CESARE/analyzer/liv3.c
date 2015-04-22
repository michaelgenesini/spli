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
  
  //increasing counter
  counter.lvl3++;

  switch(type) {
    // IPv4
    case 0x800:
      if(!r_ipv4)
        return;
      //printf("\n\nIPV4\n\n");
      //increase counter
      counter.ipv4++;
      //start decoding ipv4
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
      proto=*(p+9); //PROBABILMENTE a p + 14 + 9 vedo il protocollo livello 4
      len=ntohs(*(u_int *)(p+2));
      ihl=((*p)&0x0f)*4;
      fragm=ntohs(*(u_int *)(p+6));
      if(p_ipv4) {
        //colore(3);
        //myprintf("IPv4 |"); //MODIFICATO myprintf
        //print_ipv4(p+12);
        //myprintf(" -> "); //MODIFICATO myprintf
        //print_ipv4(p+16);
        //myprintf(" Id:%d Ttl:%d Proto:%d Len:%d",id,ttl,proto,len); //MODIFICATO myprintf
        //if(fragm&0x4000)
          //myprintf(" DF"); //MODIFICATO myprintf
        //myprintf(" Fragm:%d%c\n",fragm&0x1fff,(fragm&0x2000)?'M':'F'); //MODIFICATO myprintf
      }
      if(flag) {
        filt_kill=1;
        return;
      }
      liv4(proto,len-ihl,p+ihl, id);
      return;
    // IP v6
    case 0x86dd:
      if(!r_ipv6)
        return;
      //printf("\n\nIPV6\n\n");
      //increase counter
      counter.ipv6++;
      //start decoding 
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
        //colore(3);
        //myprintf("IPv6 |"); //MODIFICATO myprintf
        print_ipv6(p+8);
        //myprintf(" -> "); //MODIFICATO myprintf
        print_ipv6(p+24);
        //myprintf(" Proto:%d Hop:%d Len:%d Flow:%ld\n",proto,ttl,len,flow); //MODIFICATO myprintf
      }
      if(flag) {
        filt_kill=1;
        return;
      }
      liv4(proto,len-40,p+40, 0);
      return;

    case 0x0806:
      if(!p_arp) return;
      //printf("\n\nARP\n\n");
      //increase counter
      counter.arp++;
      //start decoding
      //colore(3);
      //myprintf("ARP  |"); //MODIFICATO myprintf
      switch(htons(*(u_int *)(p+6))) {
        case 1:
          //myprintf("Request   ");
          break;
        case 2:
          //myprintf("Reply     ");
          break;
        case 3:
          //myprintf("R_Request ");
          break;
        case 4:
          //myprintf("R_Reply   ");
          break;
      }
      //myprintf(" "); //MODIFICATO myprintf
      print_liv2(p+8);
      //myprintf(" -> "); //MODIFICATO myprintf
      print_liv2(p+18);
      //myprintf(" "); //MODIFICATO myprintf
      print_ipv4(p+14);
      //myprintf(" -> "); //MODIFICATO myprintf
      print_ipv4(p+24);
      //myprintf("\n"); //MODIFICATO myprintf
      decoded=1;
      return;

    default:
      //increasing counter
      counter.unknown++;
      unknown=1;
      return;
    }
}