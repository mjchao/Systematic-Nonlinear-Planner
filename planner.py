from configure import *
from structures import *
from variables import *
from topsort import *
from read import *
from Queue import PriorityQueue
import copy

MAX_SEARCH_EFFORT = 1000000

'''
Returns an estimate of the number of steps
that will be required to complete a partial
plan. This is the heuristic function
'''
def estimateRemainingCost( plan ):
    return len( plan.steps )

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
        
        #printVerbosePlan( nextPlan , tracker )
                
        #if the ordering isn't consistent, clearly this plan won't work
        if ( not isOrderConsistent( nextPlan.orderings , len( nextPlan.steps ) ) ):
            continue
        
        #if the plan is complete, then we're done
        if ( nextPlan.is_complete() ):
            return nextPlan
        
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
    
    print "FAILED" 
    raise plan_not_found()
