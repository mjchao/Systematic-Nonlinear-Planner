'''
main.py
--------
Implements the main function, which takes files as command line arguments

You need to implement two functions:
"planSearch" in planner.py (SNLP / Partial order planning)
"Action::adds(...)" in structures.py

These will probably require you to write major helper functions,
which you will document in your answer to the first question in the spec
'''

import sys

from structures import *
from configure import *
from variables import *
from read import *
from topsort import *
from planner import *


## argv[1] is the input file name
## argv[2] is the output file name
## usage: python main.py <inputfile> <outputfile>

if len(sys.argv) < 3:
    print "Not enough arguments\n"
    sys.exit()


initial = Plan()
tracker = VariableTracker()

if not readfile(sys.argv[1], initial, tracker)[0]:
    print "Could not read file\n"
    sys.exit()

print initial.open_conditions

finalPlan = Plan()
'''
try:
    finalPlan = planSearch(initial, tracker)
except:
    print "Could not find a plan\n"
    sys.exit()
'''
finalPlan = planSearch( initial , tracker )
printPlan(finalPlan, tracker)


