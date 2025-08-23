"""
Home to all the algorithms for path finding
Path v1: finished on 6/12
- basic Dijkstra's algorithm produces path and weight from grid() output
Path v2: 6/17
- Added messages in the assert statements for better debugging
"""
from .Grid import *
import math

def Dij(grid,start,target):
    """
    Practice for coding Dijkstra's algorithm to prepare for doing the actual one.
    Returns the shortest path from the start node to the target node and its distance.

    Param Grid: the graph or grid that you are using for the algorithm
    Precond: Grid is a dict of nodes with neighbors

    Param start: the starting tile or unit or node or whatever
    Precond: the starting tile must be a 2D tuple in Grid

    Param target: the taget tile or unit or node or whatever
    Precond: same as start
    """
    assert start in grid, "Start not in grid"
    assert target in grid, "Target not in grid"
    assert isinstance(start, tuple) and isinstance(target,tuple), "Either start or target is not a tuple"
    strt = grid[start] #ALSO A DICT!
    tgt = grid[target]
    dist = {}
    #Assigning original weights
    for node in grid:
        if node != start:
            dist[node] = float('inf')
        else:
            dist[node] = 0
    prev = {}
    queue = [start]
    visited = set()
    #Neighbor visiting for the start node
    for arc in strt:
        if strt[arc] < dist[arc]: #weights
            dist[arc] = strt[arc]
            prev[arc] = start
            queue.append(arc)
    visited.add(start)
    #main loop: finding the nearest neighbors repeadedly and distances
    while len(queue) > 0:
        #finding the nearest neighbor
        bestdist = float('inf')
        bestnode = None
        for sum in queue:
            if sum not in visited:
                if dist[sum] < bestdist:
                    bestdist = dist[sum]
                    bestnode = sum
        if bestnode is None:
            break
        #bestnode is the nearest neighbor and bestdist is the distance
        for i in grid[bestnode]:
            if grid[bestnode][i] + dist[bestnode] < dist[i]:
                dist[i] = grid[bestnode][i] + dist[bestnode]
                prev[i] = bestnode
                if i not in queue:
                    queue.append(i)
        queue.remove(bestnode)
        visited.add(bestnode)
    #path reconstruction
    grandTotal = target
    path = []
    while target in prev:
        path.insert(0,prev[target])
        target = prev[target]
    path.append(grandTotal)
    return path, dist[grandTotal]

def getDistance(one,two):
    """
    Returns the euclidean distance between one tuple and another (2D)

    Param one: the first 2D tuple to find the distance from
    Precond: one is a tuple of len 2 with numbers as its values

    Param two: the second 2D tuple ot find the distance from
    Precond: same as one
    """
    assert isinstance(one,tuple) and isinstance(two,tuple), "Either one or two are not tuples"
    assert len(one) == len(two) == 2, "lengths of 1 and 2 are different or are not 2"
    assert isinstance(one[0],(int,float)) and isinstance(one[1],(int,float)) and isinstance(two[0],(int,float)) and isinstance(two[1],(int,float)), "invalid component type (not int or float)"
    subx = two[0] - one[0]
    suby = two[1] - one[1]
    return math.sqrt(subx**2+suby**2)

def toRad(deg):
    """
    Degrees to Radians converter because I'm lazy. Returns the deg parameter
    converted into radians.

    Parameter deg: degree value to be converted
    Precond: deg is a number (int or float)
    """
    assert isinstance(deg,(int,float)), "invalid type for deg"
    return deg*(math.pi/180)
