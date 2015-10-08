#include "variables.h"
#include <sstream>
#include <iostream>
using namespace std;

VariableTracker::VariableTracker() {
	locationEnd = 0;
	robotEnd = 0;
	craneEnd = 0;
	pileEnd = 0;
	containerEnd = 0;
	groundEnd = 0;
}

	// Construct a literal / variable tracker
VariableTracker::VariableTracker(int numLocs, int numRobots, int numCranes,
	int numPiles, int numContainers) {
	locationEnd = numLocs;
	robotEnd = numRobots+locationEnd;
	craneEnd = numCranes + robotEnd;
	pileEnd = numPiles + craneEnd;
	containerEnd = numContainers + pileEnd;
	groundEnd = containerEnd + 1;
}

// Get the unique integer id associated with name of variable or literal
int VariableTracker::getId(string var) const {
	istringstream instr(var);
	char ch;
	int num;
	instr >> ch >> num;
	switch(ch){
		case 'l': //location
			return num;
		case 'r': //robot
			return locationEnd+num;
		case 'k': //crane
			return robotEnd+num;
		case 'p': //pile
			return craneEnd+num;
		case 'c': //container
			return pileEnd+num;
		case 'G': //ground
			return containerEnd;
		case 'x': //variable
			return groundEnd+num;
		default:
			cerr << "Invalid literal\n";
			return -1;
	};
}

// Get the name of the variable or literal associated with id
string VariableTracker::getName(int n) const {
	ostringstream varName;
	if (n < 0) varName << "InvalidVariable";
	else if (n < locationEnd) varName << 'l' << n;
	else if (n < robotEnd) varName << 'r' << n-locationEnd;
	else if (n < craneEnd) varName << 'k' << n-robotEnd;
	else if (n < pileEnd) varName << 'p' << n-craneEnd;
	else if (n < containerEnd) varName << 'c' << n-pileEnd;
	else if (n < groundEnd) varName << 'G';
	else varName << 'x' << n-groundEnd;
	return varName.str();
}