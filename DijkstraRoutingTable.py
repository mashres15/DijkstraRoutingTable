# MANIZ SHRESTHA
# LAB: DIJKSTRA'S ALGORITHM
# NETWORKS AND NETWORKING

# Dijkstra's algorithm for shortest paths
# priorityDictionary importe from David Eppstein, UC Irvine, 4 April 2002
# http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/117228
# Priority dictionary using binary heaps
"""The priority Dictionary class is credited to David Eppstein"""

#---------------------------------PRIORITY DICTIONARY------------------------------------------------------
from __future__ import generators

class priorityDictionary(dict):
    def __init__(self):
        '''Initialize priorityDictionary by creating binary heap
of pairs (value,key).  Note that changing or removing a dict entry will
not remove the old pair from the heap until it is found by smallest() or
until the heap is rebuilt.'''
        self.__heap = []
        dict.__init__(self)

    def smallest(self):
        '''Find smallest item after removing deleted items from heap.'''
        if len(self) == 0:
            raise (IndexError, "smallest of empty priorityDictionary")
        heap = self.__heap
        while heap[0][1] not in self or self[heap[0][1]] != heap[0][0]:
            lastItem = heap.pop()
            insertionPoint = 0
            while 1:
                smallChild = 2*insertionPoint+1
                if smallChild+1 < len(heap) and \
                        heap[smallChild] > heap[smallChild+1]:
                    smallChild += 1
                if smallChild >= len(heap) or lastItem <= heap[smallChild]:
                    heap[insertionPoint] = lastItem
                    break
                heap[insertionPoint] = heap[smallChild]
                insertionPoint = smallChild
        return heap[0][1]

    def __iter__(self):
        '''Create destructive sorted iterator of priorityDictionary.'''
        def iterfn():
            while len(self) > 0:
                x = self.smallest()
                yield x
                del self[x]
        return iterfn()

    def __setitem__(self,key,val):
        '''Change value stored in dictionary and add corresponding
pair to heap.  Rebuilds the heap if the number of deleted items grows
too large, to avoid memory leakage.'''
        dict.__setitem__(self,key,val)
        heap = self.__heap
        if len(heap) > 2 * len(self):
            self.__heap = [(v,k) for k,v in self.iteritems()]
            self.__heap.sort()  # builtin sort likely faster than O(n) heapify
        else:
            newPair = (val,key)
            insertionPoint = len(heap)
            heap.append(None)
            while insertionPoint > 0 and \
                    newPair < heap[(insertionPoint-1)//2]:
                heap[insertionPoint] = heap[(insertionPoint-1)//2]
                insertionPoint = (insertionPoint-1)//2
            heap[insertionPoint] = newPair

    def setdefault(self,key,val):
        '''Reimplement setdefault to call our customized __setitem__.'''
        if key not in self:
            self[key] = val
        return self[key]

    
#---------------------------------DIJKSTRA ALGORITHM------------------------------------------------------

"""Dijkstra that return dict of final distances and Predecessors"""
def Dijkstra(G,start,end=None):
    
    D = {}	# dictionary of final distances
    P = {}	# dictionary of predecessors
    Q = priorityDictionary()   # est.dist. of non-final vert.
    Q[start] = 0
    
    for v in Q:
        D[v] = Q[v]
        if v == end: break

        for w in G[v]:
            vwLength = D[v] + G[v][w]
            if w in D:
                if vwLength < D[w]:
                    raise (ValueError, \
  "Dijkstra: found better path to already-final vertex")
            elif w not in Q or vwLength < Q[w]:
                Q[w] = vwLength
                P[w] = v

    return (D,P)

#---------------------------------SHORTEST PATH METHOD--------------------------------------------------

"""ShortestPath method to generate the cost and next hop from start to end"""
def shortestPath(G,start,end):
    # Output Cost, Next Hop
    
    D,P = Dijkstra(G,start,end)
    end2 = end
    Path = []
    while 1:
        Path.append(end)
        if end == start: break
        end = P[end]
    Path.reverse()
    if len(Path)>1:
        return D[end2], Path[1]
    else:
        return D[end2], Path[0]


#---------------------------------CONSTRUCTING GRAPH--------------------------------------------------
filename ="zero.net"
file = open(filename,'r') #Opening file
print("Executing for", filename)
G ={}
for line in file:  #Reading the data in each line
    words = line.split()
    #print(words)
    # Making entries in the dictionary/Graph
    if words[0] not in G:
        G[words[0]] = {words[1]:int(words[2])}
        G[words[0]].update({words[0]:0})
        if words[1] not in G:
            G[words[1]] = {words[0]:int(words[2])}
            G[words[1]].update({words[1]:0})
        else:
            G[words[1]].update({words[0]:int(words[2])})
            
    else:
        G[words[0]].update({words[1]:int(words[2])})
        if words[1] not in G:
            G[words[1]] = {words[0]:int(words[2])}
            G[words[1]].update({words[1]:0})
        else:
            G[words[1]].update({words[0]:int(words[2])})

            
#--------------------------------------------OUTPUT---------------------------------------
print("---------------")                     
print("Printing Graph")
print("---------------") 
print(G)
print()

print("-------------")   
print("Routing table")
print("-------------")
# Iterating over each vertex in graph to produce the routing table
for i in G:
    print()
    for j in G:
        Cost, Route = shortestPath(G,i,j)
        print("Source:", i, "... Destination:", j, "... Route:", Route, "... Cost:", Cost,)
        

