"""
Patch notes:
Rover v1: finished on 6/17
- Basic rover that works and follows path with a precision of .1 tiles.
- Works on large grids.
- No working progress bar
Rover v2: finished on 6/18
- messages in the assert statements for better debugging
- higher precision (.001 tiles)
- working progress bar
Rover v3: finished on 6/19
- velocity changes based on the type of terrain rover is going through
- Max speed changed from 10 to 1
"""


from .Grid import *
from .Path import *
import numpy as np
class Rover():
    """
    The actual Rover that will be moving. It is a simple rover for now, it can't do anything but move. and face a direction and be somewhere
    """
    #Attributes and invariants: FILL IN THIS IF IT GOES ON RESUME
    #position: the position of the Rover
    #invar: position must be a coordinate (maybe used from a default value)
    #Getters and setters:
    def getProgress(self):
        """
        Returns the progress AS A PERCENTAGE
        """
        if self.progress/self.progneed < 1:
            return str(round((self.progress/self.progneed)*100,2)) + '%'
        else:
            return '100%'
    def getFacing(self):
        """
        Returns the facing of the rover in radians AND degrees
        """
        return self.facing, self.facing*(180/np.pi)

    def setFacing(self,new):
        """
        Sets a new facing value in RADIANS

        Param new: the new angle relative to the positive horizontal IN DEGREES
        Precond: new in [0,45,90,135,180,225,270,315]
        """
        assert new in [0,45,90,135,180,225,270,315], "new not in [0,45,90,135,180,225,270,315]"
        self.facing = toRad(new)

    def angleSetter(self,delta):
        """
        Sets a new facing angle for the rover based off delta
        """
        assert isinstance(delta,tuple) and isinstance(delta[0],(float,int)) and isinstance(delta[1],(float,int)), "invalid delta"
        theta = np.arctan2(delta[1],delta[0]) #returns in radians
        self.facing = theta

    def getVelocity(self):
        '''
        Returns the velocity of the rover rounded to the third decimal place (thousandths)
        '''
        return (round(self.velocity[0],3),round(self.velocity[1],3))


    def __init__(self,grid,pos=(0,0),facing=0,speed=1,targettile=None):
        """
        Initiazlises the rover in all its glory.

        Param grid: the grid that the rover will be traversing
        Precond: grid is an output from the grid() function from Grid.py

        Param pos: the position of the rover
        Precond: pos is a 2D tuple within the grid

        Param facing: the direction the rover is facing relative to the vertical IN DEGREES
        Precond: must be an int in [0,45,90,135,180,225,270,315]

        Param speed: the speed of the rover
        Precond: speed is a float or int >0 and <1

        Param targettile: the target tile of the rover (its final destination)
        Precond: targettile is a 2D tuple within the grid
        """
        #grid asserts:
        assert isinstance(grid,dict), "Grid is not a dict and is invalid (from rover)"
        for key,val in grid.items():
            assert isinstance(key,tuple) and isinstance(val,str), "the values in grid are not strings (from rover)"
            assert val in deflist, "the strings in grid are not in deflist (invalid terrain types) (from rover)"
        #everything else asserts:
        assert isinstance(pos,tuple) and isinstance(pos[0],int) and isinstance(pos[1],int), "Pos is either not a tuple or its components are not ints"
        assert facing in [0,45,90,135,180,225,270,315], "facing not in [0,45,90,135,180,225,270,315]"
        assert isinstance(speed,(int,float)) and 0<speed<=1, "Invalid speed"
        assert isinstance(targettile,tuple) and targettile in grid, "Invalid targettile"
        self.grid = grid
        self.position = pos
        self.facing = toRad(facing)
        self.starttile = pos
        self.targettile = targettile
        self.progress = 0
        self.progneed = getDistance(self.starttile,self.targettile)
        path = Dij(DijFormatter(grid),self.position,targettile)
        self.pathlen = path[1]
        self.path = path[0]
        self.speed = speed
        self.velocity = [0,0]
        self.nexttile = None
        self.currenttile = None
        self.moving = False
        self.terrain = None

    def update(self,dt):
        if self.starttile == self.targettile:
          raise Exception('Starttile is the same as targettile')
        if self.targettile is not None and self.path is not None:
            #making sure its moving and setting all its values up:
            self.moving = True
            #ensuring that the nexttile doesn't become the currenttile because it is in the path:
            if len(self.path) > 0 and self.position == self.path[0]:
                self.path.pop(0)
            #setting the angle of facing, these combinations should be the only ones true
            #as the nexttile must be bordering the currenttile
            if self.nexttile is None:
                self.nexttile = self.path.pop(0)
            #prevct = self.currenttile
            if self.currenttile is None:
                self.currenttile = self.position
            #if self.currenttile != prevct:
            if tupleSubtracter(self.nexttile,self.currenttile) in borderlist:
                delta = tupleSubtracter(self.nexttile,self.position)
                self.facing = np.arctan2(delta[1],delta[0])
            elif tupleSubtracter(self.nexttile,self.currenttile) == (0,0):
                raise Exception("Nexttile is the same as Currenttile")
            else:
                raise Exception("Nexttile is not bordering Curenttile")
            #updating the rover's position based on velocity
            ingrid = (np.trunc(self.position[0]),np.trunc(self.position[1])) #node #
            self.terrain = self.grid[ingrid] #terrain type (str)
            idx = deflist.index(self.terrain) #index
            self.velocity[0] = dt*self.speed*np.cos(self.facing)*(1/defcostlist[idx])
            self.velocity[1] = dt*self.speed*np.sin(self.facing)*(1/defcostlist[idx])
            self.position = tupleAdder(self.position,self.velocity)
            self.progress = self.progneed - getDistance(self.position,self.targettile)
            #if the rover has reached the next tile in the sequence
            if getDistance(self.position,self.nexttile) < .001: #precision of up to .001 tile guaranteed basically
                self.currenttile = self.nexttile
                if len(self.path) > 0:
                    self.nexttile = self.path.pop(0)
            if self.nexttile not in self.grid or self.currenttile not in self.grid or (np.trunc(self.position[0]),np.trunc(self.position[1])) not in self.grid:
                raise Exception("Where are you going?")
            if self.currenttile == self.targettile:
                self.velocity = [0,0]
                self.moving = False
                self.progress = self.progneed
                print(f"The rover has successfully traversed {self.pathlen} units of distance, and reached the target tile using the shortest path!")
