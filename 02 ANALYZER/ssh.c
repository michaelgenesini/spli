#include "my.h"
#include<string.h>

void parse20(int offset,const u_char *p){

	myprintf("SSH_MSG_KEXINIT\n");
	
	char descLen[10][50] = {"kex_algorithms_length", "server_host_key_algorithms_lenght", "encryption_algorithms_client_to_server_length", "encryption_algorithms_server_to_client_length", "mac_algorithms_client_to_server_length", "mac_algorithms_server_to_client_length", "compression_algorithms_client_to_server_length","compression_algorithms_server_to_client_length","languages_client_to_server_length","languages_server_to_client_length"};
	char descStr[10][50] = {"kex_algorithms_string", "server_host_key_algorithms_string", "encryption_algorithms_client_to_server_string", "encryption_algorithms_server_to_client_string", "mac_algorithms_client_to_server_string", "mac_algorithms_server_to_client_string","compression_algorithms_client_to_server_string","compression_algorithms_server_to_client_string","languages_client_to_server_string","languages_server_to_client_string"};

	myprintf("Cookie\t|");
	for (int i = 0; i < 16; ++i) {
		myprintf("%x", *(p+offset+i));
	}
	offset+=16;
	for (int i = 0; i < 10; ++i) {
		u_int lenght = ntohl(*(u_int *)(p+offset));
		offset+=4;
		myprintf("\n%s\n\t| %d\n%s\n\t|",descLen[i],lenght,descStr[i]);
		for (int j = 0; j < lenght+1; ++j) {
			myprintf("%c", *(p+offset+j));
			if(((j+1)%70)==0) {
				myprintf("\n\t|");
			}
		}
		offset+=lenght;
	}
	myprintf("\nKEX First Packet Follows\n");
	myprintf("\t| %c", *(p+offset));
	offset++;
	myprintf("\nReserved\n\t|");
	for (int i = 0; i < 4; ++i) {
		myprintf("%x", *(p+offset+i));
	}
	offset+=4;
	// Manca il padding string ma possiamo fare a meno
}

void parse34(int offset,const u_char *p){

	myprintf("DIFFIE-HELLMAN GROUP EXCHANGE REQUEST");
	u_int gexMin = ntohl(*(u_int *)(p+offset));
	offset+=4;
	myprintf("\ndh_gex_Min\t|%d",gexMin);
	u_int gexNum = ntohl(*(u_int *)(p+offset));
	offset+=4;
	myprintf("\ndh_gex_NumOfBits|%d",gexNum);
	u_int gexMax = ntohl(*(u_int *)(p+offset));
	offset+=4;
	myprintf("\ndh_gex_Max\t|%d",gexMax);
}

void parse31(int offset,const u_char *p){

	myprintf("DIFFIE-HELLMAN GROUP EXCHANGE GROUP");
	u_int multiInt = ntohl(*(u_int *)(p+offset));
	offset+=4;
	myprintf("\nmpint_length\t|%d",multiInt);
	myprintf("\ndh modulus(P)\t|");
	for (int i = 0; i < multiInt+1; ++i) {
		myprintf("%x",*(p+offset+i));
		if(((i+1)%70)==0) {
			myprintf("\n\t\t|");
		}
	}
	offset+=multiInt;
	u_int multiInt2 = ntohl(*(u_int *)(p+offset));
	offset+=4;
	myprintf("\nmpint_length\t|%d\ndh base (G)\t|",multiInt2);
	for (int i = 0; i < multiInt2; ++i) {
		myprintf("%d",*(p+offset+i));
	}
}

void parse32(int offset,const u_char *p){

	myprintf("DIFFIE-HELLMAN GROUP EXCHANGE INIT");
	u_int multiInt = ntohl(*(u_int *)(p+offset));
	offset+=4;
	myprintf("\nmpint_length\t|%d",multiInt);
	myprintf("\ndh client(e)\t|");
	for (int i = 0; i < multiInt+1; ++i) {
		myprintf("%x",*(p+offset+i));
		if(((i+1)%70)==0) {
			myprintf("\n\t\t|");
		}
	}
}

void parse33(int offset,const u_char *p){

	myprintf("DIFFIE-HELLMAN GROUP EXCHANGE REPLY");
	u_int multiInt = ntohl(*(u_int *)(p+offset));
	offset+=4;
	myprintf("\nkexdh_host_key_length\t|%d",multiInt);
	myprintf("\nkexdh_host_key\t\t|");
	for (int i = 0; i < multiInt+1; ++i) {
		myprintf("%x",*(p+offset+i));
		if(((i+1)%70)==0) {
			myprintf("\n\t\t\t|");
		}
	}
	offset+=multiInt;
	u_int multiInt2 = ntohl(*(u_int *)(p+offset));
	offset+=4;
	myprintf("\nmpint_length\t\t|%d\ndh server (f)\t\t|",multiInt2);
	for (int k = 0; k < multiInt2; ++k) {
		myprintf("%x",*(p+offset+k));
		if(((k+1)%70)==0) {
			myprintf("\n\t\t\t|");
		}
	}
	offset+=multiInt2;
	u_int multiInt3 = ntohl(*(u_int *)(p+offset));
	offset+=4;
	myprintf("\nkexdh_h_sig_length\t|%d\nkexdh_h_sig\t\t|",multiInt3);
	for (int n = 0; n < multiInt3; ++n) {
		myprintf("%x",*(p+offset+n));
		if(((i+1)%70)==0) {
			myprintf("\n\t\t\t|");
		}
	}
}

void readPayload(int offset,const u_char *p){
	u_char messCode =*(p+offset);
	myprintf("Message Code\t| %d -> ",messCode);
	offset++;
	switch(messCode){
		case 20:
			parse20(offset,p);
			break;
		case 34:
			parse34(offset,p);
			break;
		case 31:
			parse31(offset,p);
			break;
		case 32:
			parse32(offset,p);
			break;
		case 33:
			parse33(offset,p);
			break;
	}
}

void ssh(u_int len,const u_char *p) {

	int offset = 0;

	char tmp[3] = "";
	for (int i = 0; i < 3; ++i) {
		append(tmp,*(p+i));
	}

	if (strcmp(tmp,"SSH")==0) {
		myprintf("SSH Version Exchange\n");
		myprintf("Protocol: ");
		for (int i = 0; i < len; ++i) {
			myprintf("%c", *(p+offset));
			offset++;
		}
		myprintf("\n");
		
	}else{
		myprintf("SSH Binary Packet Protocol\n");
		// v
		// |00|00|06|34|06|14|..|..|..//
		// leggo un uint32
		// v-- -- -- --
		// |00|00|06|34|06|14|..|..|..
		// 
		u_int packetLenght = ntohl(*(u_int *)(p));
		myprintf("Packet Lenght\t| %d\n",packetLenght);
		offset+=4;
		
		// avendo letto 4 byte ora mi sposto avanti di 4 e leggo un byte (char)
		//  -- -- -- --v
		// |00|00|06|34|06|14|..|..|..
		//
		u_char paddingLenght =*(p+offset);
		myprintf("Padding Lenght\t| %d\n",paddingLenght);
		offset++;

		int payload = packetLenght-((int)paddingLenght)-1;
		myprintf("Payload\t\t| %d\n",payload);
		myprintf("--------------------------\n");
		// 
		// ORA LEGGO IL PAYLOAD
		// 
		if (len>=1440 && sshHolder.flag==0) {
			myprintf("###### MTU greater than 1500 ######\n");
			//sshHolder.pointer = (u_char*) malloc(sizeof(u_char)*strlen(p)+1);
  			//memcpy(sshHolder.pointer, p, strlen(p)+1);
  			sshHolder.flag=1;
		}else{
			if (sshHolder.flag==1) {
				myprintf("Devo appendere il vecchio pacchetto con quello nuovo\n");
				//readPayload(offset,p);
				sshHolder.flag=0;
			}else{
				readPayload(offset,p);
			}
			
		}

    }
}