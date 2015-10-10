from configure import *
from structures import *
from variables import *
from topsort import *
from read import *

## May find it useful to define a maximum search effort, e.g.
## MAX_SEARCH_EFFORT = 1000000


## ***** Implement Partial Order / SNLP planning here
## Take an initial partial plan, and a variable tracker,
## return a complete plan
## p is a Plan object
## tracker is a VariableTracker object
def planSearch(p, tracker):
    for cond in p.open_conditions:
        print cond 
    return p
