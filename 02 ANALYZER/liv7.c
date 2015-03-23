#include "my.h"
#include<string.h>
#define LIV7_BUFFER_SIZE 2000;

void liv7(u_int len,const u_char *p) {
	char buffer_liv7[2000] = "";
	int i = 1;
	if((int)len<=0) return;
	//increasing counter
	counter.lvl7++;
	int not_readable = 0;
	colore(5);
	myprintf("APPL |");
	for(i = 1; i <= len; i++) {
		if(isprint(*p)) {
			append(buffer_liv7, *p);
			myprintf("%c", *p);
			not_readable = 0;
		} else {
			append(buffer_liv7, " ");
			myprintf(" ");
			not_readable++;
		}
		if(isascii(*p)) {
			fprintf(mem, "%c", *p);
			not_readable = 0;
		} else {
			fprintf(mem,".");
			not_readable++;
		}
		p++;
		if (not_readable > 100) break;
		if((i%70)==0) {
			myprintf("\n     |");
		}
	}
	append(buffer_liv7, "EOP"); //adding endofpacket to end of string;

	//bisogna provare a capire quale protocollo di livello 7 abbiamo davanti
	if (r_ws) {
		if (strstr(buffer_liv7, "websocket") != NULL) {
			colore(6);
			myprintf("\nWebsocket communication\n");
			char* res = "";
			extractString(buffer_liv7, "HTTP", "Upgrade:", res);
			myprintf("\n %s", res);
			/*char** tokens;
			tokens = str_split(buffer_liv7, ':');
			int i;
			for (i = 0; *(tokens + i); i++)
			{
					printf("month=[%s]\n", *(tokens + i));
					free(*(tokens + i));
			}
			printf("\n");
			free(tokens);*/
		}
	}
	if (r_ssh) {
		//qui dobbiamo mostrare qualcosa per ssh
	}
	//resetting default color
	colore(1);
	myprintf("\n");
	fflush(mem);
	decoded=1;
}
