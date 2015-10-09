'''
variables.py
------------
Implements a class that keeps track of variable names
'''

'''
VariableTracker
---------------
In our model, all variables and ground literals are uniquely
represented as integers.

VariableTracker provides an interface that maps back-and-forth
between variable names like "c0, p1" and their unique integer identifiers

It works like this:
All integers x
0 <= x <= numLocs+numRobots+numCranes+numPiles+numContainers+1
are ground literals.
Any higher integers are variables. Integers below 0 are invalid.

If for example, we have
locationEnd <= x < robotEnd
then we know that x is a robot r with number = x - locationEnd
So locationEnd = 4, robotEnd = 15, then integer 11 represents the robot r7

All you need to know is how to construct a variable tracker 
and use its provided functions.
'''

class VariableTracker:

    ## Construct a VariableTracker object
    def __init__(self, numLocs=0, numRobots=0, numCranes=0, numPiles=0, numContainers=0):
        self.locationEnd = numLocs
        self.robotEnd = numRobots + self.locationEnd
        self.craneEnd = numCranes + self.robotEnd
        self.pileEnd = numPiles + self.craneEnd
        self.containerEnd = numContainers + self.pileEnd
        self.groundEnd = self.containerEnd + 1

    ## Get the unique integer id of a variable or literal
    def getId(self, var):
        ch = var[0]
        if ( ch != 'G' ):
            num = int(var[1])

        if ch == 'l': ## location
            return num
        elif ch == 'r': ## robot
            return self.locationEnd + num
        elif ch == 'k': ## crane
            return self.robotEnd + num
        elif ch == 'p': ## pile
            return self.craneEnd + num
        elif ch == 'c': ## container
            return self.pileEnd + num
        elif ch == 'G': ## ground
            return self.containerEnd
        elif ch == 'x': ## variable
            return self.groundEnd + num
        else:
            print "Invalid literal\n"
            return -1


    ## Get the name of the variable associated with id (n)
    def getName(self, n):
        varName = ''
        if n < 0: varName = "InvalidVariable"
        elif n < self.locationEnd: varName = 'l' + str(n)
        elif n < self.robotEnd: varName = 'r' + str(n - self.locationEnd)
        elif n < self.craneEnd: varName = 'k' + str(n - self.robotEnd)
        elif n < self.pileEnd: varName = 'p' + str(n - self.craneEnd)
        elif n < self.containerEnd: varName = 'c' + str(n - self.pileEnd)
        elif n < self.groundEnd: varName = 'G'
        else: varName = 'x' + str(n - self.groundEnd)
        return varName


    ## Get the integer value of the first variable
    def getFirstVar(self):
        return self.groundEnd

    ## Returns true if id (n) is a valid literal or variable
    def isValid(self, n):
        return (n >= 0)

    ## Returns true if v is a variable
    def isVariable(self, v):
        return (v >= self.groundEnd)

    ## Returns true if l is a literal
    def isLiteral(self, l):
        return (l < self.groundEnd and l >= 0)



