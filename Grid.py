"""
Ahmed Arif's basic rover simulation. Creates a grid with random terrain types and finds the most time efficient path.
Can convert that grid into a valid format for my Dijkstra's algorithm funciton in the Path module.
Also has some other helper functions for the main ones.
Start date: 6/10/2025.
Grid v1: finished on 6/11/25
- Basic grid for the rover created with 3 different types of terrain
- some helper functions used throughout the whole RoverSim
Grid v2: finished 6/17/25
 - added messages in the assert statements for better debugging of the other modules
 - added rounding features to tupleAdder() and tupleSubtracter()
Grid v3: finished 6/19/25
- fixed some docstrings
"""
import random as rd

#default terrain types:
d1 = 'flat dirt'
d2 = 'sand'
d3 = 'rocky'

#Costs per terrain type:
d1cost = 1
d2cost = 5
d3cost = 1

deflist = [d1,d2,d3] #ADD TO THIS LIST AS MORE DEFAULTS ARE ADDED
defcostlist = [d1cost,d2cost,d3cost]
defdict = dict(zip(deflist, defcostlist))
borderlist = [(0,1),(1,0),(1,1),(-1,0),(0,-1),(-1,-1),(-1,1),(1,-1)]


def randomDefault():
    """
    Returns a random default from the default terrain types in the form d<randomint>.

    Ex:
    randomDefault() could return d2.
    """
    return rd.choice(deflist)

def tupleAdder(tup1,tup2,round=False):
    """
    Returns 2 added tuples (or lists) together as a tuple.
    In order to add them together it just adds their x and y components together.

    For simplicity, this is for 2D tuples

    Param tup1: a 2D tuple to add
    Precond: tup1 must be a tuple or list of length 2

    Param tup2: the other 2D tuple to add
    Precond: same as tup1

    Param round: whether or not to round to 4 decimal places
    Precond: round is a bool
    """
    #return (tup1[0]+tup2[0],tup1[1]+tup2[1])
    assert isinstance(tup1,(tuple,list)) and isinstance(tup2,(tuple,list)), "tup1 or tup2 is not a tuple or a list"
    assert isinstance(tup1[0],(float,int)) and isinstance(tup1[1],(float,int)) and isinstance(tup2[0],(float,int)) and isinstance(tup2[1],(float,int)), "The components of either tup1 or tup2 are not ints or floats"
    assert isinstance(round,bool), "Round is not a bool"
    if round == False:
        return (tup1[0]+tup2[0],tup1[1]+tup2[1])
    else:
        return (round(float(tup1[0]),4)+round(float(tup2[0]),4),round(float(tup1[1]),4)+round(float(tup2[1]),4))

def tupleSubtracter(tup1,tup2,round=False):
    """
    Returns 2 subtracted tuples or lists.
    In order to subtract them it just subtracts their x and y components.
    The order is tup1-tup2

    For simplicity, this is for 2D tuples

    Param tup1: a 2D tuple or list to subtract
    Precond: tup1 must be a tuple or list of length 2

    Param tup2: the other 2D tuple or list to subtract
    Precond: same as tup1
    """
    assert isinstance(tup1,(tuple,list)) and isinstance(tup2,(tuple,list)), "tup1 or tup2 is not a tuple or a list"
    assert isinstance(tup1[0],(float,int)) and isinstance(tup1[1],(float,int)) and isinstance(tup2[0],(float,int)) and isinstance(tup2[1],(float,int)), "The components of either tup1 or tup2 are not ints or floats"
    assert isinstance(round,bool), "Round is not a bool"
    if round == False:
        return (tup1[0]-tup2[0],tup1[1]-tup2[1])
    else:
        return (round(float(tup1[0]),4)-round(float(tup2[0]),4),round(float(tup1[1]),4)-round(float(tup2[1]),4))

def Grid(x,y,randomize=False):
    """
    Defines and returns a 2D grid for the rover to traverse as an array that looks like a grid using the default terrain type.
    Each tile is labelled by its corresponding node.
    If randomize is True then the grids will have a random terrain based on the default terrain types.

    Parameter x: width of the grid in units
    Precond: x must be an int > 0

    Parameter y: length of grid in units
    Precond: same as x

    Ex: Grid(3,3) returns:
    {(0, 0): 'sand', (0, 1): 'rocky', (0, 2): 'rocky',
    (1, 0): 'rocky', (1, 1): 'sand', (1, 2): 'rocky',
    (2, 0): 'sand', (2, 1): 'rocky', (2, 2): 'flat dirt'}

    if the default terrain type is 'flat dirt'.
    """
    assert isinstance(x,int) and x > 0, "width x is not an int"
    assert isinstance(y,int) and y > 0, "height y is not an int"
    width = {}
    tuples = []
    for row in range(y):
        for col in range(x):
          tuples.append((row,col))
    for tup in tuples:
        if randomize == False:
            width[tup] = d1
        else:
            width[tup] = randomDefault()
    return width

def DijFormatter(grid):
    """
    Uses an input from Grid() and formats it by adding neighbors so that it can be used in Dij().

    Param grid: the grid from the output of Grid()
    Precond: must be an output from grid()

    Ex input:
    {
    (0, 0): 'sand', (0, 1): 'flat dirt', (0, 2): 'rocky',
    (1, 0): 'flat dirt', (1, 1): 'rocky', (1, 2): 'flat dirt',
    (2, 0): 'sand', (2, 1): 'flat dirt', (2, 2): 'rocky'
    }

    Ex output:
    {
    (0, 0): {(1, 0): 1, (0, 1): 5},
    (1, 0): {(0, 0): 1, (2, 0): 3, (1, 1): 1},
    (2, 0): {(1, 0): 3, (2, 1): 9},

    (0, 1): {(0, 0): 5, (0, 2): 1, (1, 1): 1},
    (1, 1): {(1, 0): 1, (1, 2): 3, (0, 1): 1, (2, 1): 1},
    (2, 1): {(2, 0): 9, (2, 2): 9, (1, 1): 1},

    (0, 2): {(0, 1): 1, (1, 2): 3},
    (1, 2): {(0, 2): 3, (2, 2): 9, (1, 1): 3},
    (2, 2): {(2, 1): 9, (1, 2): 9}
    }
    """
    assert isinstance(grid,dict), "grid is not a dict (from grid)"
    for key,val in grid.items():
        assert isinstance(key,tuple) and isinstance(val,str), "the values in grid are not strings (from grid)"
        assert val in deflist, "the strings in grid are not in deflist (invalid terrain types) (from grid)"
    output = {}
    save = []
    for s in grid:
        save.append(s)
    for tup,stri in grid.items():
        output[tup] = stri
    for tp in output:
        output[tp] = {}
        for tpl in borderlist:
            if tupleAdder(tp,tpl) in grid:
               output[tp][tupleAdder(tp,tpl)] = defdict[grid[tupleAdder(tp,tpl)]]
    return output
