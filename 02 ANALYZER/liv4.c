#include "my.h"

void liv4(u_int type,u_int len,const u_char *p) {
  int ihl,flag,i;
  u_int dsap,ssap;
  u_long seq_num,ack_num;
  struct filt_tcp *aux_tcp;
  struct filt_udp *aux_udp;
  u_int urg;
  const u_char *mp;
  u_char ff; 
  
  switch(type) {
    case 6:
      if(!r_tcp) return;  
      ssap=ntohs(*(u_int *)p);
      dsap=ntohs(*(u_int *)(p+2));
      flag=0;
      for(aux_tcp=filt_tcp;aux_tcp!=NULL;aux_tcp=aux_tcp->next) {
        if(aux_tcp->ssap!=ssap&&aux_tcp->ssap!=0) {
          flag=1;
          continue;
        }
        if(aux_tcp->dsap!=dsap&&aux_tcp->dsap!=0) {
          flag=1;
          continue;
        }
        flag=0;
        break;
      }
      seq_num=ntohl(*(u_long *)(p+4));
      ack_num=ntohl(*(u_long *)(p+8));
      urg=ntohl(*(u_int *)(p+18));
      ihl=((*(p+12))&0xf0)/4;
      ff=*(p+13);
      if(p_tcp) {
        colore(4);
        printf("TCP  |");
        printf("%d -> %d",ssap,dsap);
        printf(" Seq:%lu",seq_num);
        if(ff&0x20)
          printf(" URG:%d",urg);
        if(ff&0x10)
          printf(" ACK:%lu",ack_num);
        if(ff&0x08)
          printf(" PSH");
        if(ff&0x04)
          printf(" RST");
        if(ff&0x02&&ack_num==0)
          printf(" REQ");
        if(ff&0x02&&ack_num==1)
          printf(" ACP");
        if(ff&0x01)
          printf(" FIN");
        printf("\n");
      }
      if(flag) {
        filt_kill=1;
        return;
      }
      liv7(len-ihl,p+ihl);
      return;

    case 17:
      if(!r_udp)
        return;  
      ssap=ntohs(*(u_int *)p);
      dsap=ntohs(*(u_int *)(p+2));
      flag=0;
      for(aux_udp=filt_udp;aux_udp!=NULL;aux_udp=aux_udp->next) {
        if(aux_udp->ssap!=ssap&&aux_udp->ssap!=0) {
          flag=1;
          continue;
        }
        if(aux_udp->dsap!=dsap&&aux_udp->dsap!=0) {
          flag=1;
          continue;
        }
        flag=0;
        break;
      }
      if(p_udp) {
        colore(4);
        printf("UDP  |");
        printf("%d -> %d",ssap,dsap);
        printf("\n");
      }
      if(flag){
        filt_kill=1;
        return;
      }
      liv7(len-8,p+8);
      return;

    case 2:
      if(!p_igmp)
        return;  
      colore(4);
      printf("IGMP |");
      switch((*p)) {
        case 0x11:
          printf("Query ");
          print_ipv4(p+4);
          break;
        case 0x12:
          printf("Report ");
          print_ipv4(p+4);
          break;
        case 0x16:
          printf("Nreport ");
          print_ipv4(p+4);
          break;
        case 0x17: 
          printf("Leave ");
          print_ipv4(p+4);
          break;
        case 0x13:
          printf("DVMRP ** ");
          break;
        case 0x14:
          printf("PIM ** ");
          break;
        case 0x1e:
          printf("MRESP ** ");
          break;
        case 0x1f:
          printf("MTRACE ** ");
          break;
        default:
          unknown=1;
          return;
      }    
     
      printf("\n");
      decoded=1;
      return;

    case 1:
      if(!p_icmp)return;  
      colore(4);
      printf("ICMP |");
      switch((*p)&0x0f){
        case 0:
          printf("Echo Reply");
          break;
        case 8:
          printf("Echo Request");
          break;
        case 13:
          printf("Timestamp Request");
          break;
        case 14:
          printf("Timestamp Reply");
          break;
        default:
          //unknown=1;
          return;
      }   
      printf("\n");
      decoded=1;
      return;

    default:
      unknown=1;
      return;
    }
}
