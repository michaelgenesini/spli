CC          = gcc
CLINKER     = $(CC)

all: ldev

ldev: ldev.o
	$(CLINKER) -o ldev ldev.o /usr/lib/libpcap.dylib


clean:
	/bin/rm -f *.o ldev


.c.o:
	$(CC) -c $*.c
