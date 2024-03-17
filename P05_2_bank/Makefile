CXXFLAGS = -I. -DICE_CPP11_MAPPING
LIBS = -lIce++11 -lpthread

OBJS = Bank.o client.o
CXXBJS = Bank.cpp Bank.h

client: $(OBJS)
	g++ -o client $(OBJS) $(LIBS)

Bank.o: Bank.cpp
	g++ -c $(CXXFLAGS) Bank.cpp

client.o: client.cpp
	g++ -c $(CXXFLAGS) client.cpp

clean:
	rm -f client $(OBJS) $(CXXBJS)
