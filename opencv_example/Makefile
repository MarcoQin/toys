CC=gcc
CFLAGS=-O2
NAME=vision
LIBS=`pkg-config --libs --cflags opencv liblo`

_OBJ = src/main.c\
	   src/osc.c

$(NAME): $(_OBJ)
	# $(CC) -o $@ $^ $(CFLAGS) $(LIBS) -D __OSC -D FULL_SCREEN
	$(CC) -o $@ $^ $(CFLAGS) $(LIBS) -D __OSC

.PHONY: clean

clean:
	rm -f $(ODIR)/*.o $(NAME)
