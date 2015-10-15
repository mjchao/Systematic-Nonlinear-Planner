'''
structures.py
-------------
Contains the following classes and typedefs:
Predicate ## A predicate, with a type and arguments
Link ## A causal link
Threat ## A threat to a causal link
thrtCmp ## A comparator allowing threat objects to be sorted
Ordering ## An ordering constraint (typedef of (int,int))
Binding ## A variable binding (typedef of (int,int))
Action ## An action, with type, arguments, add list, delete list, and others
Plan ## An object for representing partially ordered plans
plan_not_found ## an exception class
'''

from configure import *
from variables import *
from matplotlib.pyplot import thetagrids

## An object representing a predicate
## Predicates have at least one argument, and at most two
## Unused arguments are always -1.
class Predicate:
    
    '''
    We use a static variable tracker for all Predicates due to
    design flaws in the instructor provided code. There is no
    way to print the names of the arguments to this predicate
    because there is no variable tracker provided to this
    object.
    '''
    tracker = VariableTracker()
    
    def __init__(self, t, arg1 = -1, arg2 = -1):
        self.type_t = t
        self.args = []
        if ( arg1 != -1 ):
            self.args.append(arg1)
            
        if ( arg2 != -1 ) :
            self.args.append(arg2)

    def is_equal(self, p):
        return (self.type_t == p.type_t) and (self.args[0] == p.args[0]) and (self.args[1] == p.args[1])
    
    ## Perform a substitution, substituting all instances of 
    ## variable "former" with "newval"
    ## Implemented for you
    def substitute(self, former, newval):
        for i in range(len( self.args )):
            if (self.args[i] == former):
                self.args[i] = newval
    
    def __str__(self):
        argsStr = "(" + Predicate.tracker.getName( self.args[ 0 ] )
        for i in range( 1 , len( self.args ) ):
            argsStr += ", " + Predicate.tracker.getName( self.args[ i ] )
        argsStr += ")"
        return Predicate2Name[ self.type_t ] + argsStr
    
    '''
    Determines the substitutions that would make two lists of variables/literals 
    equivalent, or returns failure if this is impossible.
    
    @param x - a list of variables or literals
    @param y - another list of variables or literals to unify with x
    @param theta - the list of substitutions
    @return - the possible substitutions can make x equivalent to y
    '''
    @staticmethod
    def unify( x , y , theta , tracker ):
        #DEBUG
        if ( type(x) == list ):
            xStr = str([ (tracker.getName( int(var) ) if type(var) == int else var) for var in x ])
        else:
            xStr = tracker.getName( x ) if type(x) == int else str(x)
            
        if ( type(y) == list ):
            yStr = str([ (tracker.getName( int(var) ) if type(var) == int else var) for var in y ])
        else:
            yStr = tracker.getName( y ) if type(y) == int else str(y)   
        #print "Unify: " + xStr + " " + yStr
        
        #check for failure
        if ( theta == None ):
            return theta
        
        #if x and y are already the same,
        #then there are no substitutions required, and we are done
        if ( x == y ):
            return theta

        #if we're unifying variables, then directly unify them
        if ( type(x) == int and tracker.isVariable( int(x) ) ):
            return Predicate.unify_var( x , y , theta , tracker )
        elif( type(y) == int and tracker.isVariable( int(y) ) ):
            return Predicate.unify_var( y , x , theta , tracker )
        
        #otherwise, this is a list
        elif( type(x) == list and type(y) == list ):
            #if the argument lists are different sizes, it is clearly
            #impossible to unify
            if ( len( x ) != len( y ) ):
                theta = None
                return theta
            
            #we directly unify the first variable/literal 
            #and then continue unifying the rest of the list
            return Predicate.unify( x[1:len(x)] , y[1:len(y)] , Predicate.unify( x[0] , y[0] , theta , tracker ) , tracker )
        else:
            theta = None
            return None
      
    '''
    Returns a substitution for var and x
    '''    
    @staticmethod
    def unify_var( var , x , theta , tracker ):
        
        #check if the variable is already substituted
        for substitution in theta :
            if ( substitution[ 0 ] == var ):
                return Predicate.unify( var , substitution[ 1 ] , theta , tracker )
                break
            
        for substitution in theta:
            if ( substitution[ 0 ] == x ):
                return Predicate.unify( x , substitution[ 1 ] , theta , tracker )
                break
            
        #no occur check needed because we don't have compound expressions!
        varName = tracker.getName( var ) if type(var) == int else str(var)
        xName = tracker.getName( x ) if type(x) == int else str(x)
        theta.append( (varName , xName) )
        return theta  

## A causal link
## Consists of a predicate, a "causal step", and a "recipient step"
## "causalStep" is an integer referring to a step in a plan which
##        adds predicate "pred" in fulfillment of the preconditions of
##        of the step "recipientStep"
##    In the paper's notation:
##    causalStep -----pred-----> recipientStep
class Link:

    def __init__(self): pass

    def __init__(self, p, cstep, rstep):
        self.pred = p
        self.causalStep = cstep
        self.recipientStep = rstep


## A threat to a causal link
## Represents the fact that the step identified by "actionId"
##     deletes the predicate of the causal link "threatened"
class Threat:
    def __init__(self, thrt, act):
        self.threatened = thrt
        self.actionId = act


## Pairs representing ordering contraints and binding constraints
## The typedef is for ease of understanding
#typedef pair<int, int> Ordering;
#typedef pair<int, int> Binding;

## An object representing an action
## Actions have at least three arguments, and at most five
class Action:
    
    '''
    Action::adds
    ----
    *** You should implement this function *****

    Takes a Predicate p and a VariableTracker tracker
    Returns a list of lists of variable bindings
    Each list of bindings is one possible substitution that 
    would cause the action to add predicate p.
    
    Each list of bindings unifies p with one of the things 
    in the add list of the action.
    For example, "start" could add both "in c0 p0" and "in c1 p1"
    If you have a predicate "in x1 x2", then start could add this 
    predicate in two different ways.
    The return value would be (({x1,c0},{x2,p0}),({x1,c1},{x2,c2}))
    Where (,) is the list and {,} is a binding.

    If nothing unifies, returns an empty list of lists.
    '''
    

    def adds(self, p, tracker):
        returnList = [] ## list of list of bindings. Each binding is a pair of integers - (int, int).
    
        ''' Fill in your own code here
        Unification is required, but only between two predicates
        (so a bit simpler than the general unification algorithm in the book)

        ***IMPORTANT***
        With our representation of variables,
        always bind HIGHER to LOWER
        so if, for example, we are binding 15, 29
        we add the pair (29,15) to our binding list, 
        which can be read as "replace 29 with 15"
        '''
        for pred in self.addList:
            if ( pred.type_t == p.type_t ):
                possibleBindings = Predicate.unify( pred.args , p.args , [] , tracker )
                if ( possibleBindings != None ):
                    returnList.append( possibleBindings )

        ## ****

        return returnList


    ## ******* The rest are implemented for you ***********

    ## Constructor
    def __init__(self, t, arg1 = -1, arg2 = -1, arg3 = -1, arg4 = -1, arg5 = -1):
        
        self.args = [] ## 5 arguments
        ##type of action
        self.addList = [] ##List of added predicates
        self.deleteList = [] ##List of deleted predicates
        
        self.type_t = t
        if ( arg1 != -1 ):
            self.args.append(arg1)
            
        if ( arg2 != -1 ):
            self.args.append(arg2)
            
        if ( arg3 != -1 ):
            self.args.append(arg3)
            
        if ( arg4 != -1 ):
            self.args.append(arg4)
            
        if ( arg5 != -1 ):
            self.args.append(arg5)

        self.fillPredicates()


    ## A utility that fills addList and deleteList based on args
    ## Called in constructor, and again during variable substitution
    ## Implemented for you.
    ## This is called either during construction, or during a 
    ## variable rebinding.
    ## Clears the old lists and inserts predicates into them based on the
    ## action arguments
    ## Does nothing if action is start or finish
    def fillPredicates(self):
        self.addList = []
        self.deleteList = []
        ##self.prereqList = []

        if self.type_t == Actions.MOVE:
            '''
            move(r, l, m) # move robot r from location l to location m
                precond: adjacent(l, m), at(r, l), free(m)
                add: at(r, m), occupied(m), free(l)
                delete: occupied(l), at(r,l), free(m)
            '''
            self.addList.append(Predicate(Predicates.AT, self.args[0], self.args[2]))
            self.addList.append(Predicate(Predicates.OCCUPIED, self.args[2]))
            self.addList.append(Predicate(Predicates.FREE, self.args[1]))

            self.deleteList.append(Predicate(Predicates.OCCUPIED, self.args[1]))
            self.deleteList.append(Predicate(Predicates.AT, self.args[0], self.args[1]))
            self.deleteList.append(Predicate(Predicates.FREE, self.args[2]))

        elif self.type_t == Actions.TAKE:
            '''
            take(k,l,c,d,p) #crane k at location l takes c off of d in pile p
                precond: belong(k,l), attached(p,l), empty(k), top(c,p), on(c,d)
                add: holding(k,c), top(d,p)
                delete: empty(k), in(c,p), top(c,p), on(c,d)
            '''

            self.addList.append(Predicate(Predicates.HOLDING, self.args[0], self.args[2]))
            self.addList.append(Predicate(Predicates.TOP, self.args[3], self.args[4]))

            self.deleteList.append(Predicate(Predicates.EMPTY, self.args[0]))
            self.deleteList.append(Predicate(Predicates.IN, self.args[2], self.args[4]))
            self.deleteList.append(Predicate(Predicates.TOP, self.args[2], self.args[4]))
            self.deleteList.append(Predicate(Predicates.ON, self.args[2], self.args[3]))

        elif self.type_t == Actions.PUT:
            '''
            put(k,l,c,d,p) # crane k at location l puts c onto d in pile p
                precond: belong(k,l), attached(p,l), holding(k,c), top(d,p)
                add: empty(k), in(c,p), top(c,p), on(c,d)
                delete: holding(k,c), top(d,p)
            '''

            self.addList.append(Predicate(Predicates.EMPTY, self.args[0]))
            self.addList.append(Predicate(Predicates.IN, self.args[2], self.args[4]))
            self.addList.append(Predicate(Predicates.TOP, self.args[2], self.args[4]))
            self.addList.append(Predicate(Predicates.ON, self.args[2], self.args[3]))

            self.deleteList.append(Predicate(Predicates.HOLDING, self.args[0], self.args[2]))
            self.deleteList.append(Predicate(Predicates.TOP, self.args[3], self.args[4]))

        elif self.type_t == Actions.LOAD:
            '''
            load(k, l, c, r) # crane k at location l loads container c onto robot r
                precond: belong(k,l), holding(k,c), at(r,l), unloaded(r)
                add: empty(k), loaded(r,c)
                delete: holding(k,c), unloaded(r)
            '''

            self.addList.append(Predicate(Predicates.EMPTY, self.args[0]))
            self.addList.append(Predicate(Predicates.LOADED, self.args[3], self.args[2]))

            self.deleteList.append(Predicate(Predicates.HOLDING, self.args[0], self.args[2]))
            self.deleteList.append(Predicate(Predicates.UNLOADED, self.args[3]))

        elif self.type_t == Actions.UNLOAD:
            '''
            unload(k,l,c,r) # crane k at location l takes container c from robot r
                precond: belong(k,l), at(r,l), loaded(r,c), empty(k)
                add: holding(k,c), unloaded(r)
                delete: empty(k), loaded(r,c)
            '''

            self.addList.append(Predicate(Predicates.HOLDING, self.args[0], self.args[2]))
            self.addList.append(Predicate(Predicates.UNLOADED, self.args[3]))

            self.deleteList.append(Predicate(Predicates.EMPTY, self.args[0]))
            self.deleteList.append(Predicate(Predicates.LOADED, self.args[3], self.args[2]))

        else: pass


    ## Perform a substitution, substituting all instances of 
    ## variable "former" with "newval"
    ## Implemented for you
    def substitute(self, former, newval):
        subst = False
        for i in range(len( self.args )):
            if (self.args[i] == former):
                self.args[i] = newval
                subst = True
        if (subst): self.fillPredicates()

    ## Returns a list of predicates consisting of the prerequisites
    ## for this particular action
    def getPrereqs(self):
        prereqList = []
        if self.type_t == Actions.MOVE:
            '''
            move(r, l, m) # move robot r from location l to location m
                precond: adjacent(l, m), at(r, l), free(m)
                add: at(r, m), occupied(m), free(l)
                delete: occupied(l), at(r,l), free(m)
            '''
            prereqList.append(Predicate(Predicates.ADJACENT, self.args[1], self.args[2]))
            prereqList.append(Predicate(Predicates.AT, self.args[0], self.args[1]))
            prereqList.append(Predicate(Predicates.FREE, self.args[2]))

        elif self.type_t == Actions.TAKE:
            '''
            take(k,l,c,d,p) #crane k at location l takes c off of d in pile p
                precond: belong(k,l), attached(p,l), empty(k), top(c,p), on(c,d)
                add: holding(k,c), top(d,p)
                delete: empty(k), in(c,p), top(c,p), on(c,d)
            '''
            prereqList.append(Predicate(Predicates.BELONG, self.args[0], self.args[1]))
            prereqList.append(Predicate(Predicates.ATTACHED, self.args[4], self.args[1]))
            prereqList.append(Predicate(Predicates.EMPTY, self.args[0]))
            prereqList.append(Predicate(Predicates.TOP, self.args[2], self.args[4]))
            prereqList.append(Predicate(Predicates.ON, self.args[2], self.args[3]))

        elif self.type_t == Actions.PUT:
            '''
            put(k,l,c,d,p) # crane k at location l puts c onto d in pile p
                precond: belong(k,l), attached(p,l), holding(k,c), top(d,p)
                add: empty(k), in(c,p), top(c,p), on(c,d)
                delete: holding(k,c), top(d,p)
            '''
            prereqList.append(Predicate(Predicates.BELONG, self.args[0], self.args[1]))
            prereqList.append(Predicate(Predicates.ATTACHED, self.args[4], self.args[1]))
            prereqList.append(Predicate(Predicates.HOLDING, self.args[0], self.args[2]))
            prereqList.append(Predicate(Predicates.TOP, self.args[3], self.args[4]))

        elif self.type_t == Actions.LOAD:
            '''
            load(k, l, c, r) # crane k at location l loads container c onto robot r
                precond: belong(k,l), holding(k,c), at(r,l), unloaded(r)
                add: empty(k), loaded(r,c)
                delete: holding(k,c), unloaded(r)
            '''
            prereqList.append(Predicate(Predicates.BELONG, self.args[0], self.args[1]))
            prereqList.append(Predicate(Predicates.HOLDING, self.args[0], self.args[2]))
            prereqList.append(Predicate(Predicates.AT, self.args[3], self.args[1]))
            prereqList.append(Predicate(Predicates.UNLOADED, self.args[3]))

        elif self.type_t == Actions.UNLOAD:
            '''
            unload(k,l,c,r) # crane k at location l takes container c from robot r
                precond: belong(k,l), at(r,l), loaded(r,c), empty(k)
                add: holding(k,c), unloaded(r)
                delete: empty(k), loaded(r,c)
            '''
            prereqList.append(Predicate(Predicates.BELONG, self.args[0], self.args[1]))
            prereqList.append(Predicate(Predicates.AT, self.args[3], self.args[1]))
            prereqList.append(Predicate(Predicates.LOADED, self.args[3], self.args[2]))
            prereqList.append(Predicate(Predicates.EMPTY, self.args[0]))

        else: pass

        return prereqList


    ## Returns true if there is a variable binding in which this action deletes the predicate
    ## Probably should also return the binding itself
    ## Calls the unification algorithm
    def deletes(self, p):
        for i in range(len(self.deleteList)):
            if (self.deleteList[ i ].type_t == p.type_t):
                if (Predicate.unify( self.deleteList[ i ].args , p.args , [] , Predicate.tracker ) != None ):
                    return True
        return False
    
    def __str__(self):
        if ( len( self.args ) > 0 ):
            argsStr = "(" + Predicate.tracker.getName( self.args[ 0 ] )
            for i in range( 1 , len( self.args ) ):
                argsStr += ", " + Predicate.tracker.getName( self.args[ i ] )
            argsStr += ")"
        else:
            argsStr = "()"
        return str(Action2Name[ self.type_t ]) + argsStr


## A plan object
## We put ordering constraints into an std::set for easy element search
## We put threats into a set for easy insertion and deletion
## Everything else comes in lists
## You may want to modify this data structure, depending on how your algorithm works
## Just note that if you do so, you may also have to modify the read function
class Plan:
    
    ##The integer id of the next variable to be allocated
    ##This is important for creating actions "with fresh variables"
    nextVar = -1

    def __init__(self):
        ## Actions are uniquely identified by their index in the steps list
        self.steps = []
        self.links = [] ## Causal links
        
        #we'll represent threats as ordered triples (T , A , B) where
        #T is the integer that represents the threat action, A is the
        #integer that represents the first endpoint of the causal link
        #and B is the integer that represents the second endpoint of the
        #causal link
        self.threats = [] ## All threats to causal links
    
        ## For open conditions, we use a list of (Predicate, int)
        ## because we need to store the "parent" action of each open condition,
        ## That is, the action that requires this Predicate as a precondition.
        ## Our solution is to simply pair predicates with integer identifiers
        self.open_conditions = []
    
        self.orderings = [] ## All ordering constraints
    
    def is_threat_addressed(self , threat):
        ordering1 = (threat.actionId , threat.threatened.causalStep)
        ordering2 = (threat.threatened.recipientStep , threat.actionId)
        return ordering1 in self.orderings or ordering2 in self.orderings
    '''
    Returns if this plan is a complete plan - i.e. there are no
    open preconditions left
    '''
    def is_complete(self):
        return len( self.open_conditions ) == 0
    
    '''
    Returns if this plan has unresolved threats that threaten
    causal links. We resolve a threat by using ordering
    constraints that force the threat to come before or after
    the endpoints of the causal link.
    '''
    def has_threats(self):
        return len( self.threats ) != 0
        

## An exception class, to be thrown if your search could not find a plan
class plan_not_found:
    def __init__(self): pass

def debug_unify():
    tracker = VariableTracker( 2 , 1 , 2 , 2 , 1 )
    Predicate.tracker = tracker   
    pred1 = Predicate( Predicates.ON , 7 , 8 )
    pred2 = Predicate( Predicates.ON , 7 , 20 )
    print "Unifying " + str(pred2) + " with " + str(pred1) + ", Result: " + str(Predicate.unify( pred2.args , pred1.args , [] , tracker ))

def debug_deletes():
    tracker = VariableTracker( 1 , 0 , 1 , 3 , 3 )
    Predicate.tracker = tracker 
    takeAction = Action( Actions.TAKE , 1 , 0 , 7 , 5 , 2 )
    pred = Predicate( Predicates.EMPTY , 1 )
    print str(takeAction) + " deletes " + str( pred ) + " ? " + str(takeAction.deletes( pred )) 

'''
Unit testing
'''
def main():
    #debug_unify()
    debug_deletes()
    return
    tracker = VariableTracker( 2 , 1 , 0 , 0 , 0 )
    Predicate.tracker = tracker
    moveAction = Action( Actions.MOVE , tracker.getUnassignedVar() , tracker.getUnassignedVar() , tracker.getUnassignedVar() )
    print str( moveAction )
    pred = Predicate( Predicates.AT , "r0" , "l1" )
    for p in moveAction.addList:
        print str(p)
        
    for p in moveAction.deleteList:
        print str(p)
    print moveAction.adds( pred , tracker )
    
    failPred = Predicate( Predicates.HOLDING , "k0" , "c1" )
    print moveAction.adds( failPred , tracker )
    
    failPred = Predicate( Predicates.AT , "r0" )
    print moveAction.adds( failPred , tracker )

if __name__ == "__main__": main()


