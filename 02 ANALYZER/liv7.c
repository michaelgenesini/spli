#include "my.h"
#include<string.h>
#define LIV7_BUFFER_SIZE 2000;

void liv7(u_int len,const u_char *p) {
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
		if (strstr(buffer_liv7, "Sec-WebSocket") != NULL) {
			//abbiamo trovato un pacchetto websocket
			liv7_unknown = 0;
			myprintf("\n\n\t| Websocket communication\n");
			//riconoscimento del tipo di pacchetto websocket
			if (strstr(buffer_liv7, "HTTP/1.1 101 Switching Protocols") != NULL) {
				//handshake from server
				myprintf("\n\t| Server handshake\n");
			} else if (strstr(buffer_liv7, "GET") != NULL) {
				//handshake from client
				myprintf("\n\t| Client handshake\n");
			}
			//stampa del pacchetto websocket
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
	if (r_ssh) {
		//qui dobbiamo mostrare qualcosa per ssh
		//Se incontro un paccetto ssh, devo mettere liv7_unknown = 0;

	}

	//non abbiamo incontrato nessun pacchetto analizzabile, procedo con la stampa normale
	if (liv7_unknown) {
		colore(5);
		myprintf("APPL |");
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
