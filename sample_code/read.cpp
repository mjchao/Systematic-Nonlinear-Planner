#include "read.h"

#include <iostream>
#include <fstream>
using namespace std;

bool readfile(string filename, Plan& plan, VariableTracker& tracker) {
	ifstream infile(filename);
	if (!infile) {
		cerr << "Could not read file.\n";
		return false;
	}

	string identifier;
	int locations, robots, cranes, piles, containers;
	infile >> identifier >> locations;
	infile >> identifier >> robots;
	infile >> identifier >> cranes;
	infile >> identifier >> piles;
	infile >> identifier >> containers;

	tracker = VariableTracker(locations, robots, cranes, piles, containers);
	plan.nextVar = tracker.getFirstVar();

	Action start(START);
	Action end(FINISH);
	bool goal = false;
	while (infile) {
		infile >> ws; //Get rid of whitespace first?
		if (infile.peek() == '#') {
			getline(infile, identifier, '\n');
			continue;
		}
		infile >> identifier;
		if (!infile) continue;
		if (identifier == "initial") continue;
		if (identifier == "goal") {
			goal = true;
			continue;
		}
		Predicates id;
		try {
			id = (Predicates) Name2Predicate.at(identifier);
		}
		catch (out_of_range e) {
			cerr << "Bad identifier\n";
			return false;
		}
		Predicate newPred;
		string arg1, arg2;
		switch (id) {
			// Two-argument propositions
			case ADJACENT:
			case ATTACHED:
			case BELONG:
			case AT:
			case LOADED:
			case HOLDING:
			case IN:
			case ON:
			case TOP:
				infile >> arg1 >> arg2;
				if (!infile) {
					cerr << "Incomplete predicate\n";
					return false;
				}
				newPred = Predicate(id, tracker.getId(arg1), tracker.getId(arg2));
			break;
			// One-argument propositions
			case OCCUPIED:
			case UNLOADED:
			case EMPTY:
			case FREE:
				infile >> arg1;
				if (!infile) {
					cerr << "Incomplete predicate\n";
					return false;
				}
				newPred = Predicate(id, tracker.getId(arg1));
			break;
		};
		if (goal) plan.open.push_back(make_pair(newPred,1));
		else start.addList.push_back(newPred);
	}
	plan.steps.push_back(start);
	plan.steps.push_back(end);
	//plan.orderings.push_back(make_pair(0,1)); // start < finish
	plan.orderings.insert(Ordering(0,1));

	return true;
}

void printPredicate(ostream& out, const Predicate& p, 
	const VariableTracker& tracker) 
{
	out << Predicate2Name.at(p.type);
	for (int i = 0; i < 2; ++i) {
		if (p.args[i] < 0) break;
		out << ' ' << tracker.getName(p.args[i]);
	}
}

void printAction(ostream& out, const Action& A, 
	const VariableTracker& tracker) 
{
	out << Action2Name.at(A.type);
	for (int i = 0; i < 5; ++i) {
		if (A.args[i] < 0) break;
		out << ' ' << tracker.getName(A.args[i]);
	}
	out << '\n';
	out << "     Prereqs: ";
	vector<Predicate> prereqs = A.getPrereqs();
	for (int i = 0; i < prereqs.size(); ++i) {
		printPredicate(out, prereqs[i], tracker);
		out << ", ";
	}
	out << '\n';
	out << "     Added: ";
	for (int i = 0; i < A.addList.size(); ++i) {
		printPredicate(out, A.addList[i], tracker);
		out << ", ";
	}
	out << '\n';
	out << "     Deleted: ";
	for (int i = 0; i < A.deleteList.size(); ++i) {
		printPredicate(out, A.deleteList[i], tracker);
		out << ", ";
	}
	out << '\n';
}

void printPlan(string outfilename, const Plan& plan, const VariableTracker& tracker) {
	ofstream outfile(outfilename);
	if (outfile) {
		printPlan(outfile, plan, tracker);
	}
	else {
		cerr << "Could open output file.\n";
	}
}

void printPlan(ostream& out, const Plan& plan, const VariableTracker& tracker) {
	out << "actions\n";
	int startStep = -1, endStep = -1;
	for (int i = 0; i < plan.steps.size(); ++i) {
		const Action& act = plan.steps[i];
		if (act.type == START) startStep = i;
		if (act.type == FINISH) endStep = i;
		out << i << ' ' << Action2Name.at(act.type);
		for (int j = 0; j < 5; ++j) {
			if (act.args[j] < 0) break;
			out << ' ' << tracker.getName(act.args[j]);
		}
		out << '\n';
	}
	out << "\nconstraints\n";
	for (auto i = plan.orderings.begin(); i != plan.orderings.end(); ++i) {
		const Ordering& o = *i;
		// Skip over start / end ordering constraints
		if (o.first == startStep || o.second == endStep) continue;
		out << o.first << " < " << o.second << '\n';
	}
}

void printVerbosePlan(ostream& out, const Plan& plan, const VariableTracker& tracker) {
	out << "#Steps\n";
	for (int i = 0; i < plan.steps.size(); ++i) {
		const Action& act = plan.steps[i];
		out << i << ' ' << Action2Name.at(act.type);
		for (int j = 0; j < 5; ++j) {
			if (act.args[j] < 0) break;
			out << ' ' << tracker.getName(act.args[j]);
		}
		out << '\n';
	}
	out << "\n#Orderings\n";
	for (auto i = plan.orderings.begin(); i != plan.orderings.end(); ++i) {
		out << i->first << " < " << i->second << '\n';
	}
	out << "\n#Causal Links\n";
	for (int i = 0; i < plan.links.size(); ++i) {
		out << plan.links[i].causalStep << ", ";
		printPredicate(out, plan.links[i].pred, tracker);
		out << ", " << plan.links[i].recipientStep << '\n';
	}
	out << "\n#Threats\n";
	for (auto i = plan.threats.begin(); i != plan.threats.end(); ++i) {
		out << i->actionId << ", (";
		out << i->threatened.causalStep << ", ";
		printPredicate(out, i->threatened.pred, tracker);
		out << ", " << i->threatened.recipientStep;
		out << ")\n";
	}
	out << "\n#Open Preconditions\n";
	for (int i = 0; i < plan.open.size(); ++i) {
		printPredicate(out, plan.open[i].first, tracker);
		out << '\n';
	}
}

