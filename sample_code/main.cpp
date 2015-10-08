/*
main.cpp
--------
Implements the main function, which takes files as command line arguments

You need to implement two functions:
"planSearch" in planner.cpp (SNLP / Partial order planning)
"Action::adds(...)" in structures.cpp

These will probably require you to write major helper functions,
which you will document in your answer to the first question in the spec
*/
#include "structures.h"
#include "configure.h"
#include "variables.h"
#include "read.h"
#include "topsort.h"
#include "planner.h"

#include <iostream>

using namespace std;


// argv[1] is the input file name
// argv[2] is the output file name
// usage: ./main <inputfile> <outputfile>
int main(int argc, char** argv) {
	if (argc < 3) {
		cerr << "Not enough arguments\n";
		return 0;
	}

	Plan initial;
	VariableTracker tracker;
	if (!readfile(argv[1], initial, tracker)) {
		cerr << "Could not read file\n";
		return 0;
	}

	Plan finalPlan;
	try {
		finalPlan = planSearch(initial, tracker);
	}
	catch (plan_not_found exc) {
		cout << "Could not find a plan\n";
		return 0;
	}

	printPlan(argv[2], finalPlan, tracker);

	return 0;
}