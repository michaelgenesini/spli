#include "my.h"
#include<string.h>
#define LIV7_BUFFER_SIZE 2000;

void liv7(u_int len,const u_char *p, u_int sourcePort, u_int destPort, u_int id) {
	char buffer_liv7[2000] = "";
	int i = 1;
	int liv7_unknown = 1;

	if((int)len<=0) return;
	//increasing counter
	counter.lvl7++;

	//storing packet inside buffer
	u_char *ptr = (u_char*) malloc(sizeof(u_char)*strlen(p)+1);
  memcpy(ptr, p, strlen(p)+1);

	int not_readable = 0;
	for(i = 1; i <= len; i++) {
		if(isprint(*ptr)) {
			append(buffer_liv7, *ptr);
			not_readable = 0;
		} else {
			strcat(buffer_liv7, "|");
			not_readable++;
		}
		ptr++;
		if (not_readable > 100) break;
	}
	append(buffer_liv7, "EOP"); //adding endofpacket to end of string;

	//changing color
	colore(6);

	//bisogna provare a capire quale protocollo di livello 7 abbiamo davanti
	if (r_ws) {
		//check first char
		//questa roba è illegale
		//controlliamo se abbiamo già ricevuto un messaggio websocket
		if ((strstr(buffer_liv7, "Sec-WebSocket") != NULL) || ((destPort == wsHolder.ws_server_port) || (sourcePort == wsHolder.ws_server_port))) {
			//abbiamo trovato un pacchetto websocket
			liv7_unknown = 0;
			//flag per pacchetti ping e pong
			int ping = 0;
			int pong = 0;
			myprintf("\n\n\t| Websocket communication\n");
			//riconoscimento del tipo di pacchetto websocket
			if (strstr(buffer_liv7, "HTTP/1.1 101 Switching Protocols") != NULL) {
				//handshake from server
				myprintf("\n\t| Server handshake\n");
				//storing in ws_holder info about serever
				wsHolder.ws_server_port = sourcePort;
				myprintf("\t| Websocket server listening on port: %d\n", sourcePort);
			} else if (strstr(buffer_liv7, "GET") != NULL) {
				//handshake from client
				myprintf("\n\t| Client handshake\n");
				//storing info about client
				wsHolder.ws_client_port = sourcePort;
				myprintf("\t| Websocket server listening on port: %d\n", destPort);
			} else {
				if (sourcePort == wsHolder.ws_server_port) {
					myprintf("\t| Websocket message from server\n");
				} else {
					myprintf("\t| Websocket message from client\n");
				}
				switch((int)*(p+0)) {
					case 138: {
						myprintf("\t| PING");
						ping = 1;
						break;
					}
					case 137: {
						myprintf("\t| PONG");
						pong = 1;
						break;
					}
				}
			}
			//stampa del pacchetto websocket
			if (!ping && !pong) {
				char *token = strtok(buffer_liv7, "|");
				myprintf("\n");
				while (token != NULL) {
					if (strlen(token) != 0) {
						myprintf("\t| %s\n", token);
					}
					token = strtok(NULL, "|");
				}
			}
		}
	}
	if (r_ssh) {
    //qui dobbiamo mostrare qualcosa per ssh
		if (strstr(buffer_liv7, "SSH") != NULL) {
      myprintf("\n\n\t| SSH Version Exchange\n");
    }else{
      //Se incontro un paccetto ssh, devo mettere liv7_unknown = 0;
      int offset = 0;
      // v
      // |00|00|06|34|06|14|..|..|..//
      // leggo un uint32
      // v-- -- -- --
      // |00|00|06|34|06|14|..|..|..
      // 
      u_int packetLenght = ntohl(*(u_int *)(p));
      myprintf("Packet Lenght:%d\n",packetLenght);
      offset+=4;
      // avendo letto 4 byte ora mi sposto avanti di 4 e leggo un byte (char)
      //  -- -- -- --v
      // |00|00|06|34|06|14|..|..|..
      //
      u_char paddingLenght =*(p+offset);
      myprintf("Padding Lenght:%d\n",paddingLenght);
      offset++;

      int payload = packetLenght-((int)paddingLenght)-1;
      myprintf("Payload:%d\n",payload);
      
      printf("MESS");
      // LEGGO IL PAYLOAD
      u_char messCode =*(p+offset);
      myprintf("Message Code:%d\n",messCode);
      offset++;
      switch(messCode){
        case 20:
          myprintf("SSH_MSG_KEXINIT\n");
          // SAREBBE DA CHIAMARE LA FUNZIONE CHE PARSA QUESTO PACCHETTO
          myprintf("Cookie: ");
          for (int i = 0; i < 16; ++i) {
            myprintf("%x", *(p+offset+i));
          }
          offset+=16;

          // FIN QUI OK!
          for (int i = 0; i < 7; ++i) {
            u_int lenght = ntohl(*(u_int *)(p+offset));
            offset+=4;
            myprintf("\nLenght: %d\n", lenght);
            myprintf("Message: ");
            if (lenght>0) {
             for (int j = 0; j < lenght+1; ++j) {
                myprintf("%c", *(p+offset));
                if (j!=lenght) {
                  offset++;
                }
              }
            }
            myprintf("\n");
          }
          
          break;
        case 34:
          myprintf("DIFFIE-HELLMAN GROUP EXCHANGE REQUEST");
          // SAREBBE DA CHIAMARE LA FUNZIONE CHE PARSA QUESTO PACCHETTO
          break;
      }

    }
	}

	//non abbiamo incontrato nessun pacchetto analizzabile, procedo con la stampa normale
	if (liv7_unknown) {
		colore(5);
		myprintf("\nAPPL |");
		i = 1;
		for(i = 1; i <= len; i++) {
			if(isprint(*p)) {
				myprintf("%c", *p);
			} else {
				myprintf(" ");
			}
			if(isascii(*p)) {
				fprintf(mem, "%c", *p);
			} else {
				fprintf(mem,".");
			}
			if((i%70)==0) {
				myprintf("\n     |");
			}
			*p++;
		}
	}

	//resetting default color
	colore(1);
	myprintf("\n");
	fflush(mem);
	decoded=1;
}
