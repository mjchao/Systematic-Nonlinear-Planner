/*
structures.h
-------------
Contains the following structs and typedefs:
Predicate // A predicate, with a type and arguments
Link // A causal link
Threat // A threat to a causal link
thrtCmp // A comparator allowing threat objects to be sorted
Ordering // An ordering constraint (typedef of std::pair<int,int>)
Binding // A variable binding (typedef of std::pair<int,int>)
Action // An action, with type, arguments, add list, delete list, and others
Plan // An object for representing partially ordered plans
plan_not_found // an exception class
*/
#ifndef STRUCTURES_H
#define STRUCTURES_H

#include "configure.h"
#include "variables.h"
#include <vector>
#include <set>
using namespace std;

// An object representing a predicate
// Predicates have at least one argument, and at most two
// Unused arguments are always -1.
struct Predicate {
	int args[2];
	Predicates type;

	Predicate() {};
	
	Predicate(Predicates t, int arg1 = -1, int arg2 = -1) {
		type = t;
		args[0] = arg1;
		args[1] = arg2;
	}

	bool operator==(const Predicate& p) const {
		return (type==p.type)&&(args[0]==p.args[0])&&(args[1]==p.args[1]);
	}
};

// A causal link
// Consists of a predicate, a "causal step", and a "recipient step"
// "causalStep" is an integer referring to a step in a plan which
//		adds predicate "pred" in fulfillment of the preconditions of
//		of the step "recipientStep"
//	In the paper's notation:
//	causalStep -----pred-----> recipientStep
struct Link {
	Predicate pred;
	int causalStep;
	int recipientStep;

	Link() {};

	Link(Predicate p, int cstep, int rstep) {
		pred = p;
		causalStep = cstep;
		recipientStep = rstep;
	}
};

// A threat to a causal link
// Represents the fact that the step identified by "actionId"
// 	deletes the predicate of the causal link "threatened"
struct Threat {
	Link threatened;
	int actionId;

	Threat(Link thrt, int act) {
		threatened = thrt;
		actionId = act;
	}
};

// A comparator for Threat objects. 
// This is necessary for putting threats in an std::set
struct thrtCmp {
	thrtCmp() {};
	bool operator()(const Threat& a, const Threat& b) {
		return (a.actionId < b.actionId) ||
			   (a.actionId == b.actionId &&
			   (a.threatened.causalStep < b.threatened.causalStep ||
			   	(a.threatened.causalStep < b.threatened.causalStep &&
			   	(a.threatened.recipientStep < b.threatened.recipientStep))));
	}
};

// Pairs representing ordering contraints and binding constraints
// The typedef is for ease of understanding
typedef pair<int, int> Ordering;
typedef pair<int, int> Binding;

// An object representing an action
// Actions have at least three arguments, and at most five
struct Action {
	int args[5]; //arguments
	Actions type; //type of action
	vector<Predicate> addList; //List of added predicates
	vector<Predicate> deleteList; //List of deleted predicates

	/*
	Action::adds
	----
	*** You should implement this function in structures.cpp *****

	Takes a Predicate p and a VariableTracker tracker
	Returns a vector of vectors of bindings
	
	Each vector of bindings unifies p with one of the things 
	in the add list of the action.
	For example, "start" could add both "in c0 p0" and "in c1 p1"
	If you have a predicate "in x1 x2", then start could add this 
	predicate in two different ways.
	The return value would be (({x1,c0},{x2,p0}),({x1,c1},{x2,c2}))
	Where (,) is the vector and {,} is a binding.

	If nothing unifies, returns an empty vector of vectors.
	 */
	vector<vector<Binding> > adds(const Predicate& p, 
		const VariableTracker& tracker) const;
	
	// ******* The rest are implemented for you ***********

	// Constructor
	Action(Actions t, int arg1 = -1, int arg2 = -1,
		 int arg3 = -1, int arg4 = -1, int arg5 = -1);

	// A utility that fills addList and deleteList based on args
	// Called in constructor, and again during variable substitution
	// Implemented for you.
	void fillPredicates();

	// Perform a substitution, substituting all instances of 
	// variable "former" with "newval"
	// Implemented for you
	void substitute(int former, int newval);

	// Returns a vector of predicates consisting of the prerequisites
	// for this particular action
	vector<Predicate> getPrereqs() const;

	// Returns true if there is a variable binding in which this action deletes the predicate
	// Probably should also return the binding itself
	// Calls the unification algorithm
	bool deletes(const Predicate& p) const;
};

// A plan object
// We put ordering constraints into an std::set for easy element search
// We put threats into a set for easy insertion and deletion
// Everything else comes in vectors
// You may want to modify this data structure, depending on how your algorithm works
// Just note that if you do so, you may also have to modify the read function
struct Plan {

	// Actions are uniquely identified by their index in the steps vector
	vector<Action> steps;
	vector<Link> links; // Causal links
	set<Threat, thrtCmp> threats; // All threats to causal links

	// For open conditions, we use a vector of pair<Predicate, int>
	// because we need to store the "parent" action of each open condition,
	// That is, the action that requires this Predicate as a precondition.
	// Our solution is to simply pair predicates with integer identifiers
	vector<pair<Predicate, int> > open;

	set<Ordering> orderings; // All ordering constraints

	//The integer id of the next variable to be allocated
	//This is important for creating actions "with fresh variables"
	int nextVar; 
};


// An exception class, to be thrown if your search could not find a plan
class plan_not_found {};


#endif