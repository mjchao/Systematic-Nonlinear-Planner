#ifndef PLANNER_H
#define PLANNER_H

#include "structures.h"
#include "variables.h"

// Take an initial partial plan, and a variable tracker,
// return a complete plan
Plan planSearch(Plan p, VariableTracker tracker);


#endif