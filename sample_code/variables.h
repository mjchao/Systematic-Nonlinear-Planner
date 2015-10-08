/*
variables.h
-----------
Implements a class that keeps track of variable names
*/
#ifndef VARIABLES_H
#define VARIABLES_H

#include <string>
using namespace std;

/*
VariableTracker
---------------
In our model, all variables and ground literals are uniquely
represented as integers.

VariableTracker provides an interface that maps back-and-forth
between variable names like "c0, p1" and their unique integer identifiers

It works like this:
All integers x
0 <= x <= numLocs+numRobots+numCranes+numPiles+numContainers+1
are ground literals.
Any higher integers are variables. Integers below 0 are invalid.

If for example, we have
locationEnd <= x < robotEnd
then we know that x is a robot r with number = x - locationEnd
So locationEnd = 4, robotEnd = 15, then integer 11 represents the robot r7

All you need to know is how to construct a variable tracker 
and use its provided functions.
*/
class VariableTracker {
private:
	int locationEnd; 
	int robotEnd; 
	int craneEnd;
	int pileEnd;
	int containerEnd;
	int groundEnd;

public:
	// Construct a VariableTracker object
	VariableTracker(int numLocs, int numRobots, int numCranes,
		int numPiles, int numContainers);

	VariableTracker();

	// Get the unique integer id of a variable or literal
	int getId(string var) const;

	// Get the name of the variable associated with id
	string getName(int id) const ;

	// Get the integer value of the first variable
	int getFirstVar() const { return groundEnd; }

	// Returns true if id is a valid literal or variable
	bool isValid(int id) const { return (id >= 0); }

	// Returns true if v is a variable
	bool isVariable(int v) const { return v >= groundEnd; }

	// Returns true if l is a literal
	bool isLiteral(int l) const { return l < groundEnd && l >= 0; }
};



#endif