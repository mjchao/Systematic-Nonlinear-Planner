from configure import *
from structures import *
from variables import *
from topsort import *
from read import *
from Queue import PriorityQueue
import copy
from random import randint

MAX_LEVEL = 1000

'''
Returns an estimate of the number of steps
that will be required to complete a partial
plan. This is the heuristic function
'''
def estimateRemainingCost( plan ):
    return len( plan.steps ) + len( plan.open_conditions )

def insert_plan( pq , plan ):
    pq.put( (estimateRemainingCost( plan ) , plan) )

## ***** Implement Partial Order / SNLP planning here
## Take an initial partial plan, and a variable tracker,
## return a complete plan
## p is a Plan object
## tracker is a VariableTracker object
def planSearch(p, tracker):
    global MAX_LEVEL
    count = 0

    #start with empty priority queue
    pq = PriorityQueue()
    insert_plan( pq , p )

    level = 0
    lastNumActions = 0
    
    #we'll use A* search
    while( not pq.empty() and level < MAX_LEVEL ):
        entry = pq.get()
        nextPlan = entry[ 1 ]
        
        if len(nextPlan.steps) != lastNumActions:
            lastNumActions = len( nextPlan.steps )
            print "LEVEL: " + str(lastNumActions)
        
        printVerbosePlan( nextPlan , tracker )
                
        #if the ordering isn't consistent, clearly this plan won't work
        if ( not isOrderConsistent( nextPlan.orderings , len( nextPlan.steps ) ) ):
            continue
        
        #if the plan is complete, then we're done
        if ( nextPlan.is_complete() ):
            if ( count == 1 ):
                return nextPlan
            else:
                count += 1
                continue
        
        #otherwise, try resolving open threats
        if ( nextPlan.has_threats() ):
            threat = nextPlan.threats[ len(nextPlan.threats)-1 ]
            childPlan1 = copy.deepcopy( nextPlan )
            del childPlan1.threats[ len( childPlan1.threats )-1 ]
            
            #enforce T < A
            childPlan1.enforce_ordering( threat.actionId , threat.threatened.causalStep )     
            insert_plan( pq , childPlan1 )
            
            childPlan2 = copy.deepcopy( nextPlan )
            del childPlan2.threats[ len( childPlan2.threats)-1 ]
            
            #enforce B < T
            childPlan2.enforce_ordering( threat.threatened.recipientStep , threat.actionId ) 
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
                        pass
                    if ( len( substitutions ) > 0 ):
                        for sub in substitutions:
                            childPlan = copy.deepcopy( nextPlan )
                            a = childPlan.steps[ i ]
                            for entry in sub:
                                for action in childPlan.steps:
                                    action.substitute( tracker.getId(entry[ 0 ]) , tracker.getId(entry[ 1 ]) )
                                for cond in childPlan.open_conditions:
                                    cond[ 0 ].substitute( tracker.getId( entry[ 0 ] ) , tracker.getId( entry[ 1 ] ) )
                        
                            newLink = Link( nextPrecond[ 0 ] , i , childPlan.open_conditions[ nextPrecondIdx ][ 1 ] )
                            childPlan.links.append( newLink )
                            
                            newOrdering = (i, childPlan.open_conditions[ nextPrecondIdx ][ 1 ] )
                            childPlan.enforce_ordering( i , childPlan.open_conditions[ nextPrecondIdx ][ 1 ] )
                            del childPlan.open_conditions[ nextPrecondIdx ]   
                        
                            #calculate new threats
                            for link in childPlan.links:
                                
                                for prereq in childPlan.steps[ link.causalStep ].getPrereqs():
                                    if ( a.deletes( prereq ) ):
                                        newThreat = Threat( link , i )
                                        childPlan.threats.append( newThreat )
                                        break;
                            '''        
                            #also calculate threats from previous actions
                            for j in range(len(childPlan.steps)):
                                if ( childPlan.steps[ j ] is not a ):
                                    for prereq in a.getPrereqs():
                                        if ( childPlan.steps[ j ].deletes( prereq ) ):
                                            newThreat = Threat( newLink , j )
                                            childPlan.threats.append( newThreat )
                                            break
                            '''
            
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
                            for cond in childPlan.open_conditions:
                                cond[ 0 ].substitute( tracker.getId( entry[ 0 ] ) , tracker.getId( entry[ 1 ] ) )
                            
                        newLink = Link( nextPrecond[ 0 ] , len(childPlan.steps)-1 , nextPrecond[ 1 ] )
                        childPlan.links.append( newLink )
                        
                        childPlan.enforce_ordering( len(childPlan.steps)-1 , nextPrecond[ 1 ] )
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
                                    
                        #also add threats from previous actions
                        for j in range(len(childPlan.steps)-1):
                            if ( childPlan.steps[ j ].deletes( nextPrecond[ 0 ] ) ):
                                print str( childPlan.steps[ j ] ) + " deletes " + str( nextPrecond[ 0 ] )
                                newThreat = Threat( newLink , j )
                                childPlan.threats.append( newThreat )
                                break
                                
                        insert_plan( pq , childPlan )
    
    print "FAILED" 
    raise plan_not_found()
