objects = read.o variables.o main.o structures.o planner.o
args = -std=c++11
headers = read.h structures.h configure.h variables.h planner.h topsort.h

all: $(objects)
	g++ $(args) -o main $(objects)

main.o: $(headers) main.cpp
	g++ $(args) -c main.cpp

read.o: read.h structures.h configure.h read.cpp
	g++ $(args) -c read.cpp

variables.o: variables.h variables.cpp
	g++ $(args) -c variables.cpp

structures.o: structures.h structures.cpp
	g++ $(args) -c structures.cpp

planner.o: $(headers) planner.cpp
	g++ $(args) -c planner.cpp

clean:
	rm $(objects) main
