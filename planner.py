from configure import *
from structures import *
from variables import *
from topsort import *
from read import *
from Queue import PriorityQueue
import copy

MAX_ITERATIONS = 300000

#we will assign states to have "infinite" cost
#if the heuristic function decides that this
#plan cannot possibly be the most efficient
INFINITE_COST = 1000000

'''
Determines if the last action taken was redundant. The 
redundancy checks we make are as follows:
* putting down a block then picking it up again
* moving a robot twice in a row
* loading then unloading a block
'''
def is_redundant( lastAction , secondToLastAction ):
    #note that because our search is backwards, the
    #second to last action in the list actually comes after the
    #last action in the list, so the actions are "inverted". e.g.
    #we check for TAKE-PUT sequences instead of
    #PUT-TAKE because the actions are in reverse order
    
    #putting down a block and then picking it up again
    #is redundant
    if ( secondToLastAction.type_t == Actions.TAKE and 
         lastAction.type_t == Actions.PUT and 
         secondToLastAction.args[ 2 ] == lastAction.args[ 2 ] ):
        return True
    
    #moving the same robot twice is redundant
    if ( secondToLastAction.type_t == Actions.MOVE and 
         lastAction.type_t == Actions.MOVE and 
         secondToLastAction.args[ 0 ] == lastAction.args[ 0 ] ):
        return True
    
    #loading then unloading a block is redundant
    if ( secondToLastAction.type_t == Actions.UNLOAD and 
         lastAction.type_t == Actions.LOAD and 
         secondToLastAction.args[ 2 ] == lastAction.args[ 2 ] ):
        return True
    
'''
Returns an estimate of the number of steps
that will be required to complete a partial
plan. This is the heuristic function
'''
def estimateCost( plan ):
    goal = plan.steps[ 1 ]
    
    #first check is for redundant actions
    lastAction = plan.steps[ len( plan.steps)-1 ]
    secondToLastAction = plan.steps[ len( plan.steps)-2 ]
    
    if ( is_redundant( lastAction , secondToLastAction ) ):
        return INFINITE_COST
    
    
    return len( plan.steps ) + len( plan.open_conditions )

def insert_plan( pq , plan ):
    cost = estimateCost( plan )
    
    #if the heuristic function decides that this path
    #has no hope because it's performing redundant actions,
    #bad action sequences, etc., we'll just prune it
    if ( cost != INFINITE_COST ):
        pq.put( (cost , plan) )

## ***** Implement Partial Order / SNLP planning here
## Take an initial partial plan, and a variable tracker,
## return a complete plan
## p is a Plan object
## tracker is a VariableTracker object
def planSearch(p, tracker):

    #start with empty priority queue
    pq = PriorityQueue()
    insert_plan( pq , p )

    iterations = 0
    #we'll use A* search
    while( not pq.empty() and iterations < MAX_ITERATIONS ):
        entry = pq.get()
        nextPlan = entry[ 1 ]
        
        #printVerbosePlan( nextPlan , tracker )
                
        #if the ordering isn't consistent, clearly this plan won't work
        if ( not isOrderConsistent( nextPlan.orderings , len( nextPlan.steps ) ) ):
            continue
        
        #if the plan is complete, then we're done
        if ( nextPlan.is_complete() ):
            print "Plan found after " + str( iterations ) + " iterations"
            return nextPlan
        
        iterations += 1
        if ( iterations % 1000 == 0 ):
            print "Iterations: " + str(iterations)
        
        #otherwise, try resolving open threats
        if ( nextPlan.has_threats() ):
            threat = nextPlan.threats[ len(nextPlan.threats)-1 ]
            del nextPlan.threats[ len(nextPlan.threats)-1 ]
            
            #create a copy of the plan with the additional constraint T < A
            childPlan1 = copy.deepcopy( nextPlan )
            
            #enforce T < A
            childPlan1.enforce_ordering( threat.actionId , threat.threatened.causalStep )
                
            insert_plan( pq , childPlan1 )
            
            #create a copy of the plan with the additional constraint B < T
            childPlan2 = copy.deepcopy( nextPlan )

            #enforce B < T
            childPlan2.enforce_ordering(threat.threatened.recipientStep , threat.actionId)

            insert_plan( pq , childPlan2 )
            
        #if no threats, then pick a precondition to satisfy
        else:
            nextPrecondIdx = 0 #randint( 0 , len(nextPlan.open_conditions)-1 )
            nextPrecondTuple = nextPlan.open_conditions[ nextPrecondIdx ]
            nextPrecond = nextPrecondTuple[ 0 ]
            precondParentIdx = nextPrecondTuple[ 1 ]
            
            #remove that open precondition from the list
            del nextPlan.open_conditions[ nextPrecondIdx ]
            
            #go through all previous actions: we're going to see if we can
            #get it to link and satisfy the precondition
            for i in range( 0 , len( nextPlan.steps ) ):
                
                #but do not let an action satisfy its own precondition
                #(index 1 stores the parent index and we can't let the
                #parent satisfy its own precondition)
                if ( i != precondParentIdx ):
                    
                    #find all sets of variable bindings such that the given action adds 
                    #the open precondition
                    substitutions = nextPlan.steps[ i ].adds( nextPrecond , tracker )
                    if ( len( substitutions ) > 0 ):
                        for sub in substitutions:
                            
                            #we need to create a copy of the current action
                            #to use at the successor - otherwise, this plan will
                            #get altered on some other iteration of the search
                            childPlan = copy.deepcopy( nextPlan )
                            a = childPlan.steps[ i ]
                        
                            #add the causal link to the given precondition
                            newLink = Link( nextPrecond , i , precondParentIdx )
                            childPlan.links.append( newLink )
                            
                            #we have to enforce that this action comes before the
                            #the action that gets its precondition satisfied
                            childPlan.enforce_ordering(i, precondParentIdx )
                        
                            #perform all necessary variable bindings on the successor
                            childPlan.bind_variables( sub , tracker )

                            #calculate new threats that result from adding this new causal link.
                            #specifically, we look at previous actions and see if any of them
                            #threaten the causal link we just added
                            childPlan.calculate_threats_to_new_link( newLink )

                            #add the successor to the queue
                            insert_plan( pq , childPlan )
            
            #create a list of new potential actions
            potentialActions = [ Action( Actions.MOVE , tracker.getUnassignedVar() , tracker.getUnassignedVar() , tracker.getUnassignedVar() ) ,
                                Action( Actions.TAKE , tracker.getUnassignedVar() , tracker.getUnassignedVar() , tracker.getUnassignedVar() , tracker.getUnassignedVar() , tracker.getUnassignedVar() ) ,
                                Action( Actions.PUT , tracker.getUnassignedVar() , tracker.getUnassignedVar() , tracker.getUnassignedVar() , tracker.getUnassignedVar() , tracker.getUnassignedVar() ) ,
                                Action( Actions.LOAD , tracker.getUnassignedVar() , tracker.getUnassignedVar() , tracker.getUnassignedVar() , tracker.getUnassignedVar() ) ,
                                Action( Actions.UNLOAD , tracker.getUnassignedVar() , tracker.getUnassignedVar() , tracker.getUnassignedVar() , tracker.getUnassignedVar() )]
            
            #go through every action
            for a in potentialActions:
                
                #check if it adds the precondition we want to satisfy
                substitutions = a.adds( nextPrecond , tracker )
                if ( len( substitutions ) > 0 ):
                    
                    #if there exist variable bindings that will let us satisfy
                    #the preconditions
                    for sub in substitutions:
                        
                        #then we'll create a successor plan - but first
                        #we need to copy the current plan so that we don't
                        #get entangled references
                        childPlan = copy.deepcopy( nextPlan )
                        
                        #add the potential action to the successor plan
                        childPlan.steps.append( a )
                        
                        #add the preconditions of of the potential action
                        #to the plan's open preconditions
                        for prereq in a.getPrereqs():
                            childPlan.open_conditions.append( (prereq , len(childPlan.steps)-1) )
                            
                        #create the new causal link
                        newLink = Link( nextPrecond , len(childPlan.steps)-1 , precondParentIdx )
                        childPlan.links.append( newLink )
                        
                        #enforce that the causal step of the link
                        #comes before the recipient step
                        childPlan.enforce_ordering(len(childPlan.steps)-1 , precondParentIdx)
        
                        #perform all variable bindings in the successor
                        childPlan.bind_variables( sub , tracker )

                        #check if adding this action might threaten any 
                        #causal links already added
                        for link in childPlan.links:
                            if ( a.deletes( link.pred ) ):
                                if ( len(childPlan.steps)-1 != link.causalStep and len(childPlan.steps)-1 != link.recipientStep ):
                                    newThreat = Threat( link , len(childPlan.steps)-1 )
                                    if ( not childPlan.is_threat_addressed( newThreat ) ):
                                        childPlan.threats.append( newThreat )
                         
                        #look for previous actions that might threaten this new
                        #causal link           
                        childPlan.calculate_threats_to_new_link( newLink )
                                
                        #add the successor to the queue
                        insert_plan( pq , childPlan )
    
    if pq.empty():
        print "FAILED"
        raise plan_not_found()
    else:
        
        #return closest approximation that was found
        return pq.get()[1]
