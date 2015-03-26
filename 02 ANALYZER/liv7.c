#include "my.h"
#include<string.h>
#define LIV7_BUFFER_SIZE 2000

void liv7(u_int len,const u_char *p, u_int sourcePort, u_int destPort, u_int id) {
	char buffer_liv7[LIV7_BUFFER_SIZE] = "";
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
    liv7_unknown = 1;
    ssh(len,p);
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
