#include "my.h"
#include<string.h>

void parse20(int offset,const u_char *p){

	myprintf("----SSH_MSG_KEXINIT----\n");
	// SAREBBE DA CHIAMARE LA FUNZIONE CHE PARSA QUESTO PACCHETTO
	myprintf("Cookie\t|");
	for (int i = 0; i < 16; ++i) {
		myprintf("%x", *(p+offset+i));
	}
	offset+=16;

	// FIN QUI OK!
	u_int lenght = 0;
	for (int i = 0; i < 7; ++i) {
		if (i>=6) {
			if (isprint(*(p+offset))) {
				printf("%c\n", *(p+offset));
				offset++;
			}else{
				printf("_");
				offset++;
			}
		}else{
			lenght = ntohl(*(u_int *)(p+offset));
			offset+=4;
			myprintf("\nLenght\t|%d", lenght);
			myprintf("\nMessage\t|");
			for (int j = 0; j < lenght+1; ++j) {
				if (isprint(*(p+offset+j))) {
					myprintf("%c", *(p+offset+j));
				}
			}
			offset+=lenght;
		}
	}
}

void readPayload(int offset,const u_char *p){
	u_char messCode =*(p+offset);
	myprintf("Message Code:\t| %d ->",messCode);
	offset++;
	switch(messCode){
		case 20:
			parse20(offset,p);
			break;
		case 34:
			myprintf("DIFFIE-HELLMAN GROUP EXCHANGE REQUEST");
			// SAREBBE DA CHIAMARE LA FUNZIONE CHE PARSA QUESTO PACCHETTO
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
		// ORA LEGGO IL PAYLOAD
		// 
		printf("LEN %d, FLAG: %d\n",len,sshHolder.flag);

		if (len==1448 && sshHolder.flag==0) {
			myprintf("###### MTU greater than 1500 ######\n");
			sshHolder.pointer = (u_char*) malloc(sizeof(u_char)*strlen(p)+1);
  			memcpy(sshHolder.pointer, p, strlen(p)+1);
  			sshHolder.flag=1;
		}else{
			readPayload(offset,p);
			sshHolder.flag=0;
		}

    }
}