# Makefile for samples program

CROSS_COMPILE=
INCLUDEDIR= 
LIBDIR=
CFLAGS=-Wall
EXTRACFLAGS=-lgpg3100

CC=$(CROSS_COMPILE)gcc
LD=$(CROSS_COMPILE)ld
TARGETS = AdSampling

ifneq ($(INCLUDEDIR),)
CFLAGS += -I$(INCLUDEDIR)
endif

ifneq ($(LIBDIR),)
CFLAGS += -L$(LIBDIR)
endif

all: $(TARGETS)

%: %.c
	$(CC) $(CFLAGS) $(EXTRACFLAGS) -o $@ $<

clean: 
	rm -f $(TARGETS) *~
 
