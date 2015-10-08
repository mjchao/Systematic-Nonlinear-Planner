#include "structures.h"

// Return a vector of vectors of variable bindings
// Each vector of bindings is one possible substitution that 
// would cause the action to add predicate p.
vector<vector<Binding> > Action::adds(const Predicate& p, 
	const VariableTracker& tracker) const 
{
	vector<vector<Binding> > returnList;
	
	/**** Fill in your own code here
	Unification is required, but only between two predicates
	(so a bit simpler than the general unification algorithm in the book)

	***IMPORTANT***
	With our representation of variables,
	always bind HIGHER to LOWER
	so if, for example, we are binding 15, 29
	we add the pair {29,15} to our binding list, 
	which can be read as "replace 29 with 15"
	*/
	






	// ****

	return returnList;
}

//******The rest of these functions are implemented for you******

// Returns true if the action deletes the given predicate
// Unification should not be done here
bool Action::deletes(const Predicate& p) const {
	for (int i = 0; i < deleteList.size(); ++i) {
		if (p == deleteList[i]) return true;
	}
	return false;
}

// This is called either during construction, or during a 
// variable rebinding.
// Clears the old lists and inserts predicates into them based on the
// action arguments
// Does nothing if action is start or finish
void Action::fillPredicates() {
	addList.clear();
	deleteList.clear();
	//prereqList.clear();
	switch(type) {
		case MOVE:
		/*
		move(r, l, m) # move robot r from location l to location m
			precond: adjacent(l, m), at(r, l), free(m)
			add: at(r, m), occupied(m), free(l)
			delete: occupied(l), at(r,l), free(m)
		*/
			addList.push_back(Predicate(AT, args[0], args[2]));
			addList.push_back(Predicate(OCCUPIED, args[2]));
			addList.push_back(Predicate(FREE, args[1]));

			deleteList.push_back(Predicate(OCCUPIED, args[1]));
			deleteList.push_back(Predicate(AT, args[0], args[1]));
			deleteList.push_back(Predicate(FREE, args[2]));
		break;
		case TAKE:
		/*
		take(k,l,c,d,p) #crane k at location l takes c off of d in pile p
			precond: belong(k,l), attached(p,l), empty(k), top(c,p), on(c,d)
			add: holding(k,c), top(d,p)
			delete: empty(k), in(c,p), top(c,p), on(c,d)
		*/

			addList.push_back(Predicate(HOLDING, args[0], args[2]));
			addList.push_back(Predicate(TOP, args[3], args[4]));

			deleteList.push_back(Predicate(EMPTY, args[0]));
			deleteList.push_back(Predicate(IN, args[2], args[4]));
			deleteList.push_back(Predicate(TOP, args[2], args[4]));
			deleteList.push_back(Predicate(ON, args[2], args[3]));
		break;
		case PUT:
		/*
		put(k,l,c,d,p) # crane k at location l puts c onto d in pile p
			precond: belong(k,l), attached(p,l), holding(k,c), top(d,p)
			add: empty(k), in(c,p), top(c,p), on(c,d)
			delete: holding(k,c), top(d,p)
		*/

			addList.push_back(Predicate(EMPTY, args[0]));
			addList.push_back(Predicate(IN, args[2], args[4]));
			addList.push_back(Predicate(TOP, args[2], args[4]));
			addList.push_back(Predicate(ON, args[2], args[3]));

			deleteList.push_back(Predicate(HOLDING, args[0], args[2]));
			deleteList.push_back(Predicate(TOP, args[3], args[4]));
		break;
		case LOAD:
		/*
		load(k, l, c, r) # crane k at location l loads container c onto robot r
			precond: belong(k,l), holding(k,c), at(r,l), unloaded(r)
			add: empty(k), loaded(r,c)
			delete: holding(k,c), unloaded(r)
		*/

			addList.push_back(Predicate(EMPTY, args[0]));
			addList.push_back(Predicate(LOADED, args[3], args[2]));

			deleteList.push_back(Predicate(HOLDING, args[0], args[2]));
			deleteList.push_back(Predicate(UNLOADED, args[3]));
		break;
		case UNLOAD:
		/*
		unload(k,l,c,r) # crane k at location l takes container c from robot r
			precond: belong(k,l), at(r,l), loaded(r,c), empty(k)
			add: holding(k,c), unloaded(r)
			delete: empty(k), loaded(r,c)
		*/

			addList.push_back(Predicate(HOLDING, args[0], args[2]));
			addList.push_back(Predicate(UNLOADED, args[3]));

			deleteList.push_back(Predicate(EMPTY, args[0]));
			deleteList.push_back(Predicate(LOADED, args[3], args[2]));
		break;
		default:

		break;
	};
}

vector<Predicate> Action::getPrereqs() const {
	vector<Predicate> prereqList;
	switch(type) {
		case MOVE:
		/*
		move(r, l, m) # move robot r from location l to location m
			precond: adjacent(l, m), at(r, l), free(m)
			add: at(r, m), occupied(m), free(l)
			delete: occupied(l), at(r,l), free(m)
		*/
			prereqList.push_back(Predicate(ADJACENT, args[1], args[2]));
			prereqList.push_back(Predicate(AT, args[0], args[1]));
			prereqList.push_back(Predicate(FREE, args[2]));
		break;
		case TAKE:
		/*
		take(k,l,c,d,p) #crane k at location l takes c off of d in pile p
			precond: belong(k,l), attached(p,l), empty(k), top(c,p), on(c,d)
			add: holding(k,c), top(d,p)
			delete: empty(k), in(c,p), top(c,p), on(c,d)
		*/
			prereqList.push_back(Predicate(BELONG,args[0], args[1]));
			prereqList.push_back(Predicate(ATTACHED, args[4], args[1]));
			prereqList.push_back(Predicate(EMPTY, args[0]));
			prereqList.push_back(Predicate(TOP, args[2], args[4]));
			prereqList.push_back(Predicate(ON, args[2], args[3]));
		break;
		case PUT:
		/*
		put(k,l,c,d,p) # crane k at location l puts c onto d in pile p
			precond: belong(k,l), attached(p,l), holding(k,c), top(d,p)
			add: empty(k), in(c,p), top(c,p), on(c,d)
			delete: holding(k,c), top(d,p)
		*/
			prereqList.push_back(Predicate(BELONG, args[0], args[1]));
			prereqList.push_back(Predicate(ATTACHED, args[4], args[1]));
			prereqList.push_back(Predicate(HOLDING, args[0], args[2]));
			prereqList.push_back(Predicate(TOP, args[3], args[4]));
		break;
		case LOAD:
		/*
		load(k, l, c, r) # crane k at location l loads container c onto robot r
			precond: belong(k,l), holding(k,c), at(r,l), unloaded(r)
			add: empty(k), loaded(r,c)
			delete: holding(k,c), unloaded(r)
		*/
			prereqList.push_back(Predicate(BELONG, args[0], args[1]));
			prereqList.push_back(Predicate(HOLDING, args[0], args[2]));
			prereqList.push_back(Predicate(AT, args[3], args[1]));
			prereqList.push_back(Predicate(UNLOADED, args[3]));
		break;
		case UNLOAD:
		/*
		unload(k,l,c,r) # crane k at location l takes container c from robot r
			precond: belong(k,l), at(r,l), loaded(r,c), empty(k)
			add: holding(k,c), unloaded(r)
			delete: empty(k), loaded(r,c)
		*/
			prereqList.push_back(Predicate(BELONG, args[0], args[1]));
			prereqList.push_back(Predicate(AT, args[3], args[1]));
			prereqList.push_back(Predicate(LOADED, args[3], args[2]));
			prereqList.push_back(Predicate(EMPTY, args[0]));
		break;
		default:

		break;
	};
	return prereqList;
}


// Substitutes all instances of "former" with instances of "newval"
void Action::substitute(int former, int newval) {
	bool subst = false;
	for (int i = 0; i < 5; ++i) {
		if (args[i] == former) {
			args[i] = newval;
			subst = true;
		} 
	}
	if (subst) fillPredicates();
}

// Constructs an action
Action::Action(Actions t, int arg1, int arg2,
		 int arg3, int arg4, int arg5) {
	type = t;
	args[0] = arg1;
	args[1] = arg2;
	args[2] = arg3;
	args[3] = arg4;
	args[4] = arg5;

	fillPredicates();
}