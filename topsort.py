'''
topsort.py
----------
Contains functions "topSort" and "isOrderConsistent"
which are useful for checking order consistency and
making partially ordered plans into linear plans (for debugging)
'''


'''
Suppose you have a graph with whose vertex count is given by "numVertices",
with the vertices labeled 0, 1, 2, ..., numVertices-1
You are given a container "orderings" of ordered pairs of integer (v1, v2),
representing directed edges v1 --> v2.

The function "topSort" takes orderings and numVertices as inputs,
and returns a pair of things. The first element of the pair, 
a vector of integers, is a topological sort of the input graph.
This means that it is a linearly ordered list of integers 
s_0, s_1, ... s_numVertices such that every edge (s_i, s_j) is such that i < j

The second element of the pair is a boolean that is true if the sort was
successful, and false if unsuccessful. A sort is unsuccessful if the input
graph contains a cycle.

A plansearch is order consistent if and only if it can be successfully 
topologically sorted - hence the usefulness of this function in our project.
A topological sort is also useful for taking a partially ordered plansearch
and making it into a linear sequence of steps, for ease of reading.
'''

def topSort(orderings, numVertices):
    sorted_t = [] ## Container for topological sort of vertices
    successful = True ## Whether or not the sort was successful
    incomingEdges = {i : 0 for i in range(numVertices)} ## The number of incoming edges of all vertices

    outgoingEdges = {i : [] for i in range(numVertices)} ## List of outgoing edges per vertex
    S = [] ## Queue of vertices with no incoming edges
    remainingEdges = len(orderings) ## Number of edges remaining in graph

    ## For each vertex, create a list of children
    ## Also, keep track of the number of incoming edges for each vertex
    for i in range(len(orderings)):
        outgoingEdges[orderings[i][0]].append(orderings[i][1])
        incomingEdges[orderings[i][1]] += 1 ## Number of incoming edges

    ## Add all vertices with zero incoming edges to a queue
    for i in range(numVertices):
        if (incomingEdges[i] == 0):
            S.append(i)

    ## Perform topological sort:
    ## While the queue is not empty, take out a vertex, put it in sorted list,
    ## remove all edges emanating from it, 
    ## and add to the queue any children who now have no incoming edges
    while len(S) > 0:
        vertex = S[0]
        S.pop(0)
        sorted_t.append(vertex)
        outgoing = outgoingEdges[vertex][:]
        for o in outgoing:
            incomingEdges[o] -= 1 ## Remove an edge
            remainingEdges -= 1
            if (incomingEdges[o] == 0): S.append(o) ## Insert a vertex if no more incoming edges

    if (remainingEdges > 0): successful = False ## If edges are left, a cycle exists

    return (sorted_t, successful)


'''
The following function takes a graph, specified in the same way as above,
and returns true if it is order consistent. Otherwise, it returns false.
This function can be used to check for consistency of plans in your algorithm.
'''

def isOrderConsistent(orderings, numVertices):
    result = topSort(orderings, numVertices)
    return result[1]

'''
Unit testing to make sure instructor code is correct
'''
def main():
    print isOrderConsistent( [(0,1) , (2 , 1)] , 3 )
    #0 < 3 < 2 < 1
    print isOrderConsistent( [(0 , 1) , (0 , 1) , (0 , 1) , (2 , 1) , (0, 2) , (3, 2)] , 4)
    print isOrderConsistent( [(0 , 1) , (0 , 2) , (2 , 1) , (3 , 2)] , 4)
    print isOrderConsistent( [(0, 3), (1, 3) , (2, 3) ] , 4)
    
if __name__ == "__main__": main()

