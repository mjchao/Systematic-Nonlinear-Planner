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
    
    def __init__(self, t, arg1 = -1, arg2 = -1):
        self.type_t = t
        self.args = []
        self.args.append(arg1)
        self.args.append(arg2)

    def is_equal(self, p):
        return (self.type_t == p.type_t) and (self.args[0] == p.args[0]) and (self.args[1] == p.args[1])
    
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
        print "Unify: " + str(x) + " " + str(y)
        
        #check for failure
        if ( theta == None ):
            return theta
        
        #if x and y are already the same,
        #then there are no substitutions required, and we are done
        if ( x == y ):
            return theta

        #if we're unifying variables, then directly unify them
        if ( type(x) == int ):
            return Predicate.unify_var( x , y , theta , tracker )
        elif( type(y) == int ):
            return Predicate.unify_var( y , x , theta , tracker )
        
        #otherwise, this is a list
        
        #if the argument lists are different sizes, it is clearly
        #impossible to unify
        if ( len( x ) != len( y ) ):
            theta = None
            return theta
        
        #we directly unify the first variable/literal 
        #and then continue unifying the rest of the list
        return Predicate.unify( x[1:len(x)] , y[1:len(y)] , Predicate.unify( x[0] , y[0] , theta , tracker ) , tracker )
          
    def unify_var( self , var , x , theta , tracker ):
        
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
        theta.append( (var , x) )
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
    args = [] ## 5 arguments
    ##type of action
    addList = [] ##List of added predicates
    deleteList = [] ##List of deleted predicates
    
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
             possibleBindings = Predicate.unify( pred.args , p.args , [] , tracker )
             if ( len( possibleBindings ) > 0 ):
                 returnList.append( possibleBindings )

        ## ****

        return returnList


    ## ******* The rest are implemented for you ***********

    ## Constructor
    def __init__(self, t, arg1 = -1, arg2 = -1, arg3 = -1, arg4 = -1, arg5 = -1):
        self.type_t = t
        self.args.append(arg1)
        self.args.append(arg2)
        self.args.append(arg3)
        self.args.append(arg4)
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
        for i in range(5):
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
            if (p == self.deleteList[i]):
                return True
        return False


## A plan object
## We put ordering constraints into an std::set for easy element search
## We put threats into a set for easy insertion and deletion
## Everything else comes in lists
## You may want to modify this data structure, depending on how your algorithm works
## Just note that if you do so, you may also have to modify the read function
class Plan:

    ## Actions are uniquely identified by their index in the steps list
    steps = []
    links = [] ## Causal links
    threats = [] ## All threats to causal links

    ## For open conditions, we use a list of (Predicate, int)
    ## because we need to store the "parent" action of each open condition,
    ## That is, the action that requires this Predicate as a precondition.
    ## Our solution is to simply pair predicates with integer identifiers
    open_conditions = []

    orderings = [] ## All ordering constraints

    ##The integer id of the next variable to be allocated
    ##This is important for creating actions "with fresh variables"
    nextVar = -1


## An exception class, to be thrown if your search could not find a plan
class plan_not_found:
    def __init__(self): pass


'''
Unit testing
'''
def main():
    tracker = VariableTracker( 2 , 1 , 0 , 0 , 0 )
    moveAction = Action( Actions.MOVE )
    pred = Predicate( Predicates.AT , "r0" , "l1" )
    for p in moveAction.addList:
        print str( p.args )
    print moveAction.adds( pred , tracker )
    pass

if __name__ == "__main__": main()


