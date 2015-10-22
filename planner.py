'''
main.py
--------
Implements the main function, which takes files as command line arguments

You need to implement two functions:
"planSearch" in plansearch.py (SNLP / Partial order planning)
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
from plansearch import *


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

'''
a1 = Action( Actions.TAKE , 1 , 0 , 7 , 5 , 2 )
a2 = Action( Actions.TAKE , 1 , 0 , 6 , 8 , 2 )
a3 = Action( Actions.TAKE , 1 , 0 , 5 , 8 , 2 )
a4 = Action( Actions.PUT , 1 , 0 , 5 , 6 , 2 )
a5 = Action( Actions.PUT , 1 , 0 , 6 , 7 , 2 )
a6 = Action( Actions.PUT , 1 , 0 , 7 , 8 , 2 )
initial.steps.append( a1 )
for prereq in a1.getPrereqs():
    initial.open_conditions.append( (prereq , 2) )
initial.steps.append( a2 )
for prereq in a2.getPrereqs():
    initial.open_conditions.append( (prereq , 3) )
initial.steps.append( a3 )
for prereq in a3.getPrereqs():
    initial.open_conditions.append( (prereq , 4) )
initial.steps.append( a4 )
for prereq in a4.getPrereqs():
    initial.open_conditions.append( (prereq , 5) )
initial.steps.append( a5 )
for prereq in a5.getPrereqs():
    initial.open_conditions.append( (prereq , 6) )
initial.steps.append( a6 )
for prereq in a6.getPrereqs():
    initial.open_conditions.append( (prereq , 7) )
'''

finalPlan = Plan()
'''
try:
    finalPlan = planSearch(initial, tracker)
except:
    print "Could not find a plansearch\n"
    sys.exit()
'''
finalPlan = planSearch( initial , tracker )

print "===== FINAL PLAN====="
printVerbosePlan( finalPlan , tracker )
ordering = topSort( finalPlan.orderings , len( finalPlan.steps ) )[ 0 ]
print ordering
#printPlan(finalPlan, tracker)

#write solution to file
print "Writing solution to file..."
f = open( sys.argv[ 2 ] , "w" )
f.write( "actions\n" )
for i in range( len( finalPlan.steps ) ):
    f.write( str(i) + " " + finalPlan.steps[ i ].to_output_str() + "\n")
f.write( "\nconstraints\n" )
for order in finalPlan.orderings:
    f.write( str(order[ 0 ]) + " < " + str(order[ 1 ]) + "\n" )
f.write( "\nlinks\n" )
for link in finalPlan.links:
    f.write( str(link.causalStep) + " " + str(link.recipientStep) + " " + link.pred.to_output_str() + "\n" )
print "Done."

