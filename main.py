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

readInputStatus = readfile(sys.argv[1])
if ( not readInputStatus[ 0 ] ):
    print "Could not read file\n"
    sys.exit()

initial = readInputStatus[ 1 ]
tracker = readInputStatus[ 2 ]
Predicate.tracker = tracker
print str(initial.open_conditions[ 0 ][ 0 ])

printPlan( initial , tracker )

finalPlan = Plan()
'''
try:
    finalPlan = planSearch(initial, tracker)
except:
    print "Could not find a plan\n"
    sys.exit()
'''
finalPlan = planSearch( initial , tracker )

print "===== FINAL PLAN====="
printVerbosePlan( finalPlan , tracker )
sequence = topSort( finalPlan.orderings , len( finalPlan.steps ) )
print sequence[ 0 ]
#printPlan(finalPlan, tracker)


