"""
File to run the rover simulation.
In order to run this in the command prompt type in: python -m RoverSim
"""
from .Grid import *
from .Rover import *
from .Path import *
from .sim import *
import time
import multiprocessing
def main():
    '''
    Runs a single Rover simulation for testing
    '''
    grid = Grid(50,50, randomize=True)
    start = (0,0)
    target = (45,48)
    r = Rover(grid, pos=start, facing=0, speed=1, targettile=target)
    dt = 0.001 #a dt greater than this may cause the rover to fail and oscillate
    print(r.path)
    if r.moving == False:
        r.update(dt)  # kickstart it
    step = 0
    while r.moving:
        step += 1
        #print('Rover is moving')
        print(f"Step: {step}  Pos: {(round(r.position[0],4),round(r.position[1],4))}  facing: {(round(r.getFacing()[0],3),round(r.getFacing()[1],3))}  Prog: {r.getProgress()} ct: {r.currenttile} nt: {r.nexttile}  Terrain: {r.terrain}")
        r.update(dt)
        #time.sleep(0.01)

def main2():
    '''
    Can run multiple rover simulations side by side, but not concurrently
    (adding more rovers will increase the amount of time for testing)
    '''
    dt = 0.1

    # Create multiple simulations with different grids and rovers
    sims = []
    sizes = [20,20,20,20,20,20,20,20,20,20]  # Example grid sizes, can adjust as needed
    for size in sizes:
        grid = Grid(size, size, randomize=True)
        start = (0, 0)
        target = (size - 1, size - 1)
        rover = Rover(grid, pos=start, facing=0, speed=1, targettile=target)
        sims.append({'grid': grid, 'rover': rover})
    for sim in sims:
        rover = sim['rover']
        if rover.moving == False:
            rover.update(dt)

    all_stopped = False
    step = 0
    while not all_stopped:
        all_stopped = True  # Assume all stopped, disprove if any rover is still moving
        for i, sim in enumerate(sims):
            rover = sim['rover']
            if rover.moving:
                try:
                    print(f"Step {step} - Rover {i} on {rover.position} moving towards {rover.nexttile}")
                    rover.update(dt)
                    all_stopped = False
                except Exception as e:
                    print(f"Rover {i} error: {e}. Stopping this rover.")
                    rover.moving = False
        step += 1
    print("\n--- Simulation Summary ---")
    for i, sim in enumerate(sims):
        rover = sim['rover']
        if rover.moving == False and rover.currenttile == rover.targettile:
            print(f"Rover {i} successfully reached the target tile {rover.targettile}!")
        else:
            print(f"Rover {i} did not reach the target tile. Last tile: {rover.currenttile}")

def main3():
    '''
    Able to run multiple rover simulations concurrently.
    It's recommended not to run more processes than the amount of cores on your CPU.
    Somehow is slower than main2() so ts is useless ig.
    '''
    sizes = [20,20,20,20,20,20,20,20,20,20]

    with multiprocessing.Pool(processes=10) as pool:
        results = pool.map(run_simulation, sizes)

    for res in results:
        print(res)


if __name__ == "__main__":
    main()
