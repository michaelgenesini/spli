#include <pcap.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <netinet/in.h>
#include <netinet/if_ether.h>
#include <stdarg.h>


void ssh(u_int,const u_char *);
void liv7(u_int,const u_char *, u_int, u_int, u_int);
void liv4(u_int,u_int,const u_char *, u_int);
void liv3(u_int,const u_char *);
void liv2(u_char *,const struct pcap_pkthdr *,const u_char *);
void colore(int);
void o_colore(int);
void myprintf(const char *, ...);
void print_ipv4(const u_char *);
void print_ipv6(const u_char *);
void print_liv2(const u_char *);


typedef struct {
  //generic counters 
  int tot;
  int lvl3;
  int lvl4;
  int lvl7;
  //specific counters
  //lvl3
  int ipv4;
  int ipv6;
  int arp;
  //lvl4
  int tcp;
  int udp;
  int igmp;
  int icmp;
  int unknown;
  //lvl7
} p_counter;

typedef struct {
  u_char *pointer;
  u_int flag;
  u_int encrypted;
} ssh_holder;

typedef struct {
  u_int ws_server_port;
  u_int ws_messages_id;
  u_int ws_client_port;
} ws_holder;

struct filt_ipv4 {
  u_char sip[4];
  u_char scid;
  u_char dip[4];
  u_char dcid;
  struct filt_ipv4 *next;
};

struct filt_ipv6 {
  u_char sip[16];
  u_char scid;
  u_char dip[16];
  u_char dcid;
  struct filt_ipv6 *next;
};

struct filt_tcp {
  u_int ssap;
  u_int dsap;
  struct filt_tcp *next;
};

struct filt_udp {
  u_int ssap;
  u_int dsap;
  struct filt_udp *next;
};


extern char outbuf[];
extern int olen;
extern int p_liv2;
extern int p_ipv4;
extern int r_ipv4;
extern struct filt_ipv4 *filt_ipv4;
extern int p_ipv6;
extern int r_ipv6;
extern struct filt_ipv6 *filt_ipv6;
extern int p_udp;
extern int r_udp;
extern struct filt_udp *filt_udp;
extern int p_tcp;
extern int r_tcp;
extern struct filt_tcp *filt_tcp;
extern int p_arp;
extern int p_igmp;
extern int p_icmp;
extern int filt_kill;
extern int unknown;
extern int decoded;
extern int p_filt_kill;
extern int p_unknown;
extern int p_decoded;
extern char device[];
extern FILE *mem;
extern int r_ssh;
extern int p_ssh;
extern int r_ws;
extern int p_ws;
p_counter counter;
ws_holder wsHolder;
ssh_holder sshHolder;

extern FILE *ws_file;