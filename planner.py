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
    return len( plan.steps ) + len( plan.open_conditions )

def insert_plan( pq , plan ):
    pq.put( (estimateRemainingCost( plan ) , plan) )

## ***** Implement Partial Order / SNLP planning here
## Take an initial partial plan, and a variable tracker,
## return a complete plan
## p is a Plan object
## tracker is a VariableTracker object
def planSearch(p, tracker):

    #start with empty priority queue
    pq = PriorityQueue()
    insert_plan( pq , p )

    level = 0
    lastNumActions = 0
    #we'll use A* search
    while( not pq.empty() and level < 1000 ):
        entry = pq.get()
        nextPlan = entry[ 1 ]
        
        if len(nextPlan.steps) != lastNumActions:
            lastNumActions = len( nextPlan.steps )
            print "LEVEL: " + str(lastNumActions)
        
        #print "PROCESSING Node " + str(planId) + ":" 
        #printVerbosePlan( nextPlan , tracker )
                
        #if the ordering isn't consistent, clearly this plan won't work
        if ( not isOrderConsistent( nextPlan.orderings , len( nextPlan.steps ) ) ):
            #print "Order is not consistent"
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
                    if ( len( substitutions ) > 0 ):
                        for sub in substitutions:
                            childPlan = copy.deepcopy( nextPlan )
                            a = childPlan.steps[ i ]
                        
                            newLink = Link( nextPrecond[ 0 ] , i , childPlan.open_conditions[ nextPrecondIdx ][ 1 ] )
                            childPlan.links.append( newLink )
                            
                            for entry in sub:
                                for action in childPlan.steps:
                                    action.substitute( tracker.getId(entry[ 0 ]) , tracker.getId(entry[ 1 ]) )
                                for cond in childPlan.open_conditions:
                                    cond[ 0 ].substitute( tracker.getId( entry[ 0 ] ) , tracker.getId( entry[ 1 ] ) )
                                for link in childPlan.links:
                                    link.pred.substitute( tracker.getId( entry[ 0 ] ) , tracker.getId( entry[ 1 ] ) )
                            
                            newOrdering = (i, childPlan.open_conditions[ nextPrecondIdx ][ 1 ] )
                            if ( not newOrdering in childPlan.orderings ):
                                childPlan.orderings.append( (i , childPlan.open_conditions[ nextPrecondIdx ][ 1 ] ) )
                            del childPlan.open_conditions[ nextPrecondIdx ]   
                        
                            #calculate new threats
                            for link in childPlan.links:
                                if ( a.deletes( link.pred ) ):
                                    if ( i != link.causalStep and i != link.recipientStep ):
                                        newThreat = Threat( link , i )
                                        if ( not childPlan.is_threat_addressed( newThreat ) ):
                                            childPlan.threats.append( newThreat )
                                    
                            for j in range(len(childPlan.steps)):
                                if ( j != i and childPlan.steps[ j ].deletes( newLink.pred ) ):
                                    if ( j != link.causalStep and j != link.recipientStep ):
                                        newThreat = Threat( newLink , j )
                                        if ( not childPlan.is_threat_addressed( newThreat ) ):
                                            childPlan.threats.append( newThreat )
            
                            #print "Generated child plan " + str(idx+1) + " using past action " + str( nextPlan.steps[ i ] )
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
                            
                        newLink = Link( nextPrecond[ 0 ] , len(childPlan.steps)-1 , nextPrecond[ 1 ] )
                        childPlan.links.append( newLink )
        
                        for entry in sub:
                            for action in childPlan.steps :
                                action.substitute( tracker.getId(entry[ 0 ]) , tracker.getId(entry[ 1 ]) )
                            for cond in childPlan.open_conditions:
                                cond[ 0 ].substitute( tracker.getId( entry[ 0 ] ) , tracker.getId( entry[ 1 ] ) )
                            for link in childPlan.links:
                                link.pred.substitute( tracker.getId( entry[ 0 ] ) , tracker.getId( entry[ 1 ] ) )
                        
                        newOrdering = (len(childPlan.steps)-1 , nextPrecond[ 1 ])
                        if ( not newOrdering in childPlan.orderings ):
                            childPlan.orderings.append( newOrdering )
                        del childPlan.open_conditions[ nextPrecondIdx ]
                        
                        for precond in a.getPrereqs():
                            childPlan.open_conditions.append( (precond , len(childPlan.steps)-1) )
                        
                        #calculate new threats
                        for link in childPlan.links:
                            if ( a.deletes( link.pred ) ):
                                if ( i != link.causalStep and i != link.recipientStep ):
                                    newThreat = Threat( link , i )
                                    if ( not childPlan.is_threat_addressed( newThreat ) ):
                                        childPlan.threats.append( newThreat )
                                    
                        for j in range(len(childPlan.steps)):
                            if ( childPlan.steps[ j ].deletes( newLink.pred ) ):
                                if ( j != newLink.causalStep and j != newLink.recipientStep ):
                                    newThreat = Threat( newLink , j )
                                    if ( not childPlan.is_threat_addressed( newThreat ) ):
                                        childPlan.threats.append( newThreat )
                                
                        #print "Generated child plan " + str(idx+1) + " using " + str(a)
                        insert_plan( pq , childPlan )
    
    print "FAILED" 
    raise plan_not_found()
