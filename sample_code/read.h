/*
read.h
-------
Contains functions for reading and printing out plans
*/
#ifndef READ_H
#define READ_H

#include "structures.h"
#include "configure.h"
#include "variables.h"
#include <string>
#include <iostream>
using namespace std;

// Takes an empty plan object and an empty variable tracker
// Fills these with the info in the file specified by "filename"
bool readfile(string filename, Plan& plan, VariableTracker& tracker);

// Print a single predicate to the output stream "out"
// Maybe useful for debugging
void printPredicate(ostream& out, const Predicate& p, 
	const VariableTracker& tracker);

// Print a single action to the output stream "out"
// Maybe useful for debugging
void printAction(ostream& out, const Action& A, const VariableTracker& tracker);

// An overloaded printing function that either prints your plan to
// the output stream "out", or to the file "outfilename"
// Use these for generating output files
void printPlan(string outfilename, const Plan& plan, const VariableTracker& tracker);
void printPlan(ostream& out, const Plan& plan, const VariableTracker& tracker);

// A function that prints more information about a plan
// Possibly useful for debugging
void printVerbosePlan(ostream& out, const Plan& plan, const VariableTracker& tracker);


#endif