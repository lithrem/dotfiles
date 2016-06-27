# http://www.aktau.be/2013/08/07/a-makefile-for-modern-c-programming-on-unix-like-operating-systems/

TARGET = myapp

# if defaults not set, use sensible defaults
CC  ?= gcc
NM  ?= nm

# if $CFLAGS is not set, be very pedantic and compile
# as C11, that should catch some common errors, also
# fortify the source, which is a must for security.
HARD_CFLAGS := -fPIE -fstack-protector-strong --param=ssp-buffer-size=4
WARN_CFLAGS := -Wall               \
	-pedantic                      \
	-Wextra                        \
	-Wconversion -Wsign-conversion \
	-Wformat-security -Werror=format-security              \
	-Wcast-align -Wcast-qual       \
	-Waggregate-return             \
	-Wunreachable-code             \
	-Wfloat-equal                  \
	-Wformat=2                     \
# unreachable-code is a no op on new gcc

FEDORA_CFLAGS := -grecord-gcc-switches

#-fexceptions

CFLAGS ?= $(WARN_CFLAGS) $(HARD_CFLAGS) $(FEDORA_CFLAGS) \
	-D_FORTIFY_SOURCE=2  \
	-Wredundant-decls -Wundef \
	-Wdisabled-optimization -Wshadow -Wmissing-braces \
	-Wstrict-aliasing=2 -Wstrict-overflow=5 -Wconversion \
	-std=c11

CFLAGS_DEBUG := -g3 \
	-O              \
	-DDEBUG

CFLAGS_RELEASE := -O2 \
	-march=native     \
	-mtune=native     \
	-ftree-vectorize

LDFLAGS ?= -Wl,-z,relro,-z,now -pie

OBJECTS = $(patsubst %.c, %.o, $(wildcard *.c))
HEADERS = $(wildcard *.h)

# the default target is debug
all: debug

# when the target is debug,
# add CFLAGS_DEBUG to CFLAGS
debug: CFLAGS += $(CFLAGS_DEBUG)
debug: $(TARGET)

# when the target is release,
# add CFLAGS_RELEASE to CFLAGS
release: CFLAGS += $(CFLAGS_RELEASE)
release: $(TARGET)

$(TARGET): $(OBJECTS)
	$(CC) $(OBJECTS) -o $@ $(CFLAGS) $(LDFLAGS)

# when looking for something that ends in .o, look
# for the same thing ending in .c and run gcc on it
%.o: %.c $(HEADERS)
	$(CC) -c $< -o $@ $(CFLAGS)

%.d: %.c
	$(CPP) $(CFLAGS) $< -MM -MT $(@:.d=.o) >$@

clean:
	-rm -f *.o
	-rm -f $(TARGET)

run: $(TARGET)
	./$(TARGET)

.PRECIOUS: $(TARGET) $(OBJECTS)

.PHONY: debug release all run

