import os
import re
import tqdm
import sys
import bisect 
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
from utils import *

basepath = os.path.dirname(os.path.abspath(__file__))

for filename in ['test_input.txt', 'input.txt']:
    print(filename)
    tot = 0
    tot2 = 0

    lines = []
    grid = []
    with open(os.path.join(basepath, filename), 'r') as fin:
        lines = [x.strip() for x in fin]
        grid = [[x for x in line] for line in lines]

    grid = grid[::-1]
    start = None
    end = None
    for i,j in gridrange(grid):
        if grid[i][j] == "S":
            start = (j,i)
        if grid[i][j] == "E":
            end = (j,i)
    

    dir = (1,0)

    states = [(0, start, dir, tuple([start]))]

    cost_by_loc = {}
    best_cost = None
    best_paths = []
    while True:
        cost, loc, dir, history = state = states.pop(0)
        if best_cost and cost > best_cost:
            break
        f_loc = step(loc, dir)
        if (loc, dir) not in cost_by_loc:
            cost_by_loc[(loc, dir)] = cost
        elif cost_by_loc[(loc, dir)] < cost:
            continue
        else:
            cost_by_loc[(loc, dir)] = cost
        if f_loc == end:
            if best_cost is None:
                best_cost = cost + 1
                best_paths.append([x for x in history]+[f_loc])
            elif best_cost == cost + 1:
                best_paths.append([x for x in history]+[f_loc])
            continue
        if in_grid(grid, f_loc) and gat(grid, f_loc) != "#":
            bisect.insort(states, (cost+1, f_loc, dir, tuple([x for x in history]+[f_loc])))
        l_dir = turn(dir, left=True)
        r_dir = turn(dir, left=False)
        l_loc = step(loc, l_dir)
        r_loc = step(loc, r_dir)
        if in_grid(grid, l_loc) and gat(grid, l_loc) != "#":
            bisect.insort(states, (cost+1001, l_loc, l_dir, tuple([x for x in history]+[l_loc])))
        if in_grid(grid, r_loc) and gat(grid, r_loc) != "#":
            bisect.insort(states, (cost+1001, r_loc, r_dir, tuple([x for x in history]+[r_loc])))

    tot = best_cost

    print(best_paths)
    path_locs = set()
    for path in best_paths:
        for loc in path:
            path_locs.add(loc)
    tot2 = len(path_locs)
    # for x, y in path_locs:
    #     grid[y][x] = "O"
    # grid = grid[::-1]
    # print_grid(grid)
    print(tot)
    print(tot2)
    # break

## Started 5 minutes late
## seemed pretty straightforward to just build up all location/direction pairs with the minimum cost to get there
## essentially just a floodfill
## got lucky that I started tracking history to debug part 1 so I could just use it for part 2
## had a skip condition on the best cost for part 1 that skipped equal cost paths for efficiency, which messed me up for a while
## and then just remembering to tack on start/end node