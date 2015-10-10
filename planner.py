from configure import *
from structures import *
from variables import *
from topsort import *
from read import *
from Queue import PriorityQueue
import copy
from random import randint

MAX_SEARCH_EFFORT = 1000000

'''
Returns an estimate of the number of steps
that will be required to complete a partial
plan. This is the heuristic function
'''
def estimateRemainingCost( plan ):
    #TODO use better heuristic
    return len( plan.open_conditions )

def insert_plan( pq , plan ):
    pq.put( (estimateRemainingCost( plan ) , plan) )

## ***** Implement Partial Order / SNLP planning here
## Take an initial partial plan, and a variable tracker,
## return a complete plan
## p is a Plan object
## tracker is a VariableTracker object
def planSearch(p, tracker):
    #for cond in p.open_conditions:
    #    print str(cond[ 0 ]) 
    
    #start with empty priority queue
    pq = PriorityQueue()
    insert_plan( pq , p )

    #we'll use A* search
    while( not pq.empty() ):
        nextPlan = pq.get()[ 1 ]
        
        print "PROCESSING: " 
        print pq.qsize()
        printVerbosePlan( nextPlan , tracker )
                
        #if the ordering isn't consistent, clearly this plan won't work
        if ( not isOrderConsistent( nextPlan.orderings , len( nextPlan.steps ) ) ):
            continue
        
        #if the plan is complete, then we're done
        if ( nextPlan.is_complete() ):
            return nextPlan
        
        #otherwise, try resolving open threats
        if ( nextPlan.has_threats() ):
            threat = nextPlan.threats[ len(nextPlan.threats)-1 ]
            childPlan1 = copy.deepcopy( nextPlan )
            del childPlan1.threats[ len( childPlan1.threats )-1 ]
            
            #enforce T < A
            childPlan1.orderings.append( ( threat.actionId , threat.threatened.causalStep ) )
            insert_plan( pq , childPlan1 )
            
            childPlan2 = copy.deepcopy( nextPlan )
            del childPlan2.threats[ len( childPlan2.threats)-1 ]
            
            #enforce B < T
            childPlan2.orderings.append( (threat.threatened.recipientStep , threat.actionId) )
            insert_plan( pq , childPlan2 )
            
        #if no threats, then pick a precondition to satisfy
        else:
            nextPrecondIdx = randint( 0 , len(nextPlan.open_conditions)-1 )
            nextPrecond = nextPlan.open_conditions[ nextPrecondIdx ]
            for i in range( 0 , len( nextPlan.steps ) ):
                a = nextPlan.steps[ i ]
                substitutions = a.adds( nextPrecond[ 0 ] , tracker )
                if ( len( substitutions ) > 0 ):
                    for sub in substitutions:
                        for entry in sub:
                            print entry
                            a.substitute( tracker.getId(entry[ 0 ]) , tracker.getId(entry[ 1 ]) )
                    childPlan = copy.deepcopy( nextPlan )
                    newLink = Link( nextPrecond[ 0 ] , i , childPlan.open_conditions[ nextPrecondIdx ][ 1 ] )
                    childPlan.links.append( newLink )
                    childPlan.orderings.append( (i , childPlan.open_conditions[ nextPrecondIdx ][ 1 ] ) )
                    del childPlan.open_conditions[ nextPrecondIdx ]   
                    
                    #calculate new threats
                    for link in childPlan.links:
                        for prereq in childPlan.steps[ link.causalStep ].getPrereqs():
                            if ( a.deletes( prereq ) ):
                                newThreat = Threat( link , i )
                                childPlan.threats.append( newThreat )
                                break;
    
                    insert_plan( pq , childPlan )
                    
            potentialActions = [ Action( Actions.MOVE , tracker.getUnassignedVar() , tracker.getUnassignedVar() , tracker.getUnassignedVar() ) ,
                                Action( Actions.TAKE , tracker.getUnassignedVar() , tracker.getUnassignedVar() , tracker.getUnassignedVar() , tracker.getUnassignedVar() , tracker.getUnassignedVar() ) ,
                                Action( Actions.PUT , tracker.getUnassignedVar() , tracker.getUnassignedVar() , tracker.getUnassignedVar() , tracker.getUnassignedVar() , tracker.getUnassignedVar() ) ,
                                Action( Actions.LOAD , tracker.getUnassignedVar() , tracker.getUnassignedVar() , tracker.getUnassignedVar() , tracker.getUnassignedVar() ) ,
                                Action( Actions.UNLOAD , tracker.getUnassignedVar() , tracker.getUnassignedVar() , tracker.getUnassignedVar() , tracker.getUnassignedVar() )]
            
            for a in potentialActions:
                substitutions = a.adds( nextPrecond[ 0 ] , tracker )
                if ( len( substitutions ) > 0 ):
                    childPlan = copy.deepcopy( nextPlan )
                    for sub in substitutions:
                        for entry in sub:
                            print entry
                            a.substitute( tracker.getId(entry[ 0 ]) , tracker.getId(entry[ 1 ]) )
                            
                    print "OK! adding " + str(a)
                    childPlan.steps.append( a )
                    newLink = Link( nextPrecond[ 0 ] , len(childPlan.steps)-1 , nextPrecond[ 1 ] )
                    childPlan.links.append( newLink )
                    childPlan.orderings.append( (len(childPlan.steps)-1 , nextPrecond[ 1 ]) )
                    del childPlan.open_conditions[ nextPrecondIdx ]
                    
                    for precond in a.getPrereqs():
                        childPlan.open_conditions.append( (precond , len(childPlan.steps)-1) )
                    
                    for link in childPlan.links:
                        for prereq in childPlan.steps[ link.causalStep ].getPrereqs():
                            if ( a.deletes( prereq ) ):
                                newThreat = Threat( link , len(childPlan.steps)-1 )
                                childPlan.threats.append( newThreat )
                                break;
                            
                    insert_plan( pq , childPlan )
    
    print "FAILED" 
    raise plan_not_found()
