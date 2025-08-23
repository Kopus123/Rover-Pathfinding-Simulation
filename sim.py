'''
Module to help main3() in __main__.py to work properly
'''
from .Grid import *
from .Rover import *
from .Path import *


def run_simulation(size):
    try:
        grid = Grid(size, size, randomize=True)
        start = (0, 0)
        target = (size - 1, size - 1)
        rover = Rover(grid, pos=start, facing=0, speed=1, targettile=target)
        print(f"Initial moving state: {rover.moving}")
        dt = 0.1
        if not rover.moving:
            rover.update(dt)
        step = 0
        if not rover.moving:
            print("Rover not moving at start!")
        while rover.moving:
            rover.update(dt)
            step += 1
            print(f"Step {step}: Position {rover.position}, moving: {rover.moving}")
        return f"Rover on {size}x{size} grid finished in {step} steps."
    except Exception as e:
        return f"Rover on {size}x{size} grid failed: {e}"
