from configure import *
from structures import *
from variables import *
from topsort import *
from read import *
from Queue import PriorityQueue
import copy
from random import randint

MAX_SEARCH_EFFORT = 1000000

idx = 0
'''
Returns an estimate of the number of steps
that will be required to complete a partial
plan. This is the heuristic function
'''
def estimateRemainingCost( plan ):
    global idx
    #TODO use better heuristic
    #e.g. number of causal links + number of open preconditions
    #return len( plan.open_conditions )
    idx = idx + 1
    return idx

def insert_plan( pq , plan ):
    pq.put( (estimateRemainingCost( plan ) , plan) )

## ***** Implement Partial Order / SNLP planning here
## Take an initial partial plan, and a variable tracker,
## return a complete plan
## p is a Plan object
## tracker is a VariableTracker object
def planSearch(p, tracker):
    global idx

    #start with empty priority queue
    pq = PriorityQueue()
    insert_plan( pq , p )
    insert_plan( pq , None )

    level = 0
    #we'll use A* search
    while( not pq.empty() ):
        entry = pq.get()
        nextPlan , planId = entry[ 1 ] , entry[ 0 ]
        if ( nextPlan is None ):
            if ( not pq.empty() ):
                insert_plan( pq , None )
            level += 1
            print "LEVEL: " + str(level)
            continue
        
        
        print "PROCESSING Node " + str(planId) + ":" 
        printVerbosePlan( nextPlan , tracker )
                
        #if the ordering isn't consistent, clearly this plan won't work
        if ( not isOrderConsistent( nextPlan.orderings , len( nextPlan.steps ) ) ):
            print "Order is not consistent"
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
            newOrdering = ( threat.actionId , threat.threatened.causalStep )
            
            #TODO create an enforceOrdering() method in plan
            if ( not newOrdering in childPlan1.orderings ):
                childPlan1.orderings.append( newOrdering )
                
            insert_plan( pq , childPlan1 )
            
            childPlan2 = copy.deepcopy( nextPlan )
            del childPlan2.threats[ len( childPlan2.threats)-1 ]
            
            #enforce B < T
            newOrdering = (threat.threatened.recipientStep , threat.actionId)
            if ( not newOrdering in childPlan2.orderings ):
                childPlan2.orderings.append( newOrdering )  
            insert_plan( pq , childPlan2 )
            
        #if no threats, then pick a precondition to satisfy
        else:
            nextPrecondIdx = 0 #randint( 0 , len(nextPlan.open_conditions)-1 )
            nextPrecond = nextPlan.open_conditions[ nextPrecondIdx ]
            for i in range( 0 , len( nextPlan.steps ) ):
                
                #do not let an action link to or threaten itself
                if ( i != nextPrecond[ 1 ] ):
                    substitutions = nextPlan.steps[ i ].adds( nextPrecond[ 0 ] , tracker )
                    if ( i == 0 ):
                        print "Unifying with start: " + str(substitutions)
                    if ( len( substitutions ) > 0 ):
                        for sub in substitutions:
                            childPlan = copy.deepcopy( nextPlan )
                            a = childPlan.steps[ i ]
                            for entry in sub:
                                for action in childPlan.steps:
                                    action.substitute( tracker.getId(entry[ 0 ]) , tracker.getId(entry[ 1 ]) )
                        
                            newLink = Link( nextPrecond[ 0 ] , i , childPlan.open_conditions[ nextPrecondIdx ][ 1 ] )
                            childPlan.links.append( newLink )
                            
                            newOrdering = (i, childPlan.open_conditions[ nextPrecondIdx ][ 1 ] )
                            if ( not newOrdering in childPlan.orderings ):
                                childPlan.orderings.append( (i , childPlan.open_conditions[ nextPrecondIdx ][ 1 ] ) )
                            del childPlan.open_conditions[ nextPrecondIdx ]   
                        
                            #calculate new threats
                            for link in childPlan.links:
                                
                                for prereq in childPlan.steps[ link.causalStep ].getPrereqs():
                                    if ( a.deletes( prereq ) ):
                                        newThreat = Threat( link , i )
                                        childPlan.threats.append( newThreat )
                                        break;
            
                            print "Generated child plan " + str(idx+1) + " using past action " + str( nextPlan.steps[ i ] )
                            insert_plan( pq , childPlan )
                    
            potentialActions = [ Action( Actions.MOVE , tracker.getUnassignedVar() , tracker.getUnassignedVar() , tracker.getUnassignedVar() ) ,
                                Action( Actions.TAKE , tracker.getUnassignedVar() , tracker.getUnassignedVar() , tracker.getUnassignedVar() , tracker.getUnassignedVar() , tracker.getUnassignedVar() ) ,
                                Action( Actions.PUT , tracker.getUnassignedVar() , tracker.getUnassignedVar() , tracker.getUnassignedVar() , tracker.getUnassignedVar() , tracker.getUnassignedVar() ) ,
                                Action( Actions.LOAD , tracker.getUnassignedVar() , tracker.getUnassignedVar() , tracker.getUnassignedVar() , tracker.getUnassignedVar() ) ,
                                Action( Actions.UNLOAD , tracker.getUnassignedVar() , tracker.getUnassignedVar() , tracker.getUnassignedVar() , tracker.getUnassignedVar() )]
            
            for a in potentialActions:
                substitutions = a.adds( nextPrecond[ 0 ] , tracker )
                if ( len( substitutions ) > 0 ):
                    for sub in substitutions:
                        childPlan = copy.deepcopy( nextPlan )
                        childPlan.steps.append( a )
                        for entry in sub:
                            for action in childPlan.steps :
                                action.substitute( tracker.getId(entry[ 0 ]) , tracker.getId(entry[ 1 ]) )
                            
                        newLink = Link( nextPrecond[ 0 ] , len(childPlan.steps)-1 , nextPrecond[ 1 ] )
                        childPlan.links.append( newLink )
                        
                        newOrdering = (len(childPlan.steps)-1 , nextPrecond[ 1 ])
                        if ( not newOrdering in childPlan.orderings ):
                            childPlan.orderings.append( newOrdering )
                        del childPlan.open_conditions[ nextPrecondIdx ]
                        
                        for precond in a.getPrereqs():
                            childPlan.open_conditions.append( (precond , len(childPlan.steps)-1) )
                        
                        #check for new threats
                        for link in childPlan.links:
                            
                            #do not let action threaten itself
                            if ( len(childPlan.steps)-1 != link.causalStep ):
                                for prereq in childPlan.steps[ link.causalStep ].getPrereqs():
                                    if ( a.deletes( prereq ) ):
                                        newThreat = Threat( link , len(childPlan.steps)-1 )
                                        childPlan.threats.append( newThreat )
                                        break;
                                
                        print "Generated child plan " + str(idx+1) + " using " + str(a)
                        insert_plan( pq , childPlan )
    
    print "FAILED" 
    raise plan_not_found()
