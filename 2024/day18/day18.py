import os
import re
import tqdm
import bisect
import sys
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
        grid = [tuple([int(x) for x in line.split(",")]) for line in lines]

    end = (70,70) if filename[0] != "t" else (6,6)

    grid2 = [["." for x in range(end[0]+1)] for y in range(end[1]+1)]
    grid = grid[:12] if filename[0] == "t" else grid[:1024]
    for x,y in grid:
        grid2[y][x] = "#"

    grid = grid2
    start = (0,0)

    states = [(0, start, tuple([start]))]

    cost_by_loc = {}
    best_cost = None
    best_paths = []
    while True:
        cost, loc, history = state = states.pop(0)
        # print(cost, loc)
        if best_cost and cost > best_cost:
            break
        if loc not in cost_by_loc:
            cost_by_loc[loc] = cost
        elif cost_by_loc[loc] <= cost:
            continue
        else:
            cost_by_loc[loc] = cost
        for n_loc in get_neighbors(grid, loc):
            if loc == end:
                if best_cost is None:
                    best_cost = cost + 1
                    best_paths.append([x for x in history]+[n_loc])
                elif best_cost == cost + 1:
                    best_paths.append([x for x in history]+[n_loc])
                continue
            if in_grid(grid, n_loc) and gat(grid, n_loc) != "#":
                bisect.insort(states, (cost+1, n_loc, tuple([x for x in history]+[n_loc])))

    tot = best_cost - 1
    print(tot)


    blocks = [tuple([int(x) for x in line.split(",")]) for line in lines]
    grid = [["." for x in range(end[0]+1)] for y in range(end[1]+1)]

    best_path = []
    for block_i in range(len(blocks)):
        block_x, block_y = blocks[block_i]
        grid[block_y][block_x] = "#"
        if best_path and (block_x, block_y) not in best_path:
            continue
        start = (0,0)

        states = [(0, start, tuple([start]))]

        cost_by_loc = {}
        best_cost = None
        while len(states):
            cost, loc, history = state = states.pop(0)
            # print(cost, loc)
            if best_cost and cost > best_cost:
                break
            if loc not in cost_by_loc:
                cost_by_loc[loc] = cost
            elif cost_by_loc[loc] <= cost:
                continue
            else:
                cost_by_loc[loc] = cost
            for n_loc in get_neighbors(grid, loc):
                if loc == end:
                    if best_cost is None:
                        best_cost = cost + 1
                        best_path = [x for x in history]+[n_loc]
                        break
                if in_grid(grid, n_loc) and gat(grid, n_loc) != "#":
                    bisect.insort(states, (cost+1, n_loc, tuple([x for x in history]+[n_loc])))
            if best_cost is not None:
                break
        if best_cost is None:
            print(block_x, ",", block_y)
            break
    # print(tot2)
    # break