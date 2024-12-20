import os
import re
import tqdm
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
        grid = [[x for x in line] for line in lines]

    grid = grid[::-1]
    start = end = None
    for i,j in gridrange(grid):
        if grid[i][j] == "S":
            start = (j,i)
        elif grid[i][j] == "E":
            end = (j, i)

    start_dist = {start: 0}
    end_dist = {end: 0}

    curr = [start]
    while curr:
        next_node = curr.pop(0)
        for nbr in get_neighbors(grid, next_node):
            if gat(grid, nbr) == "#":
                continue
            if nbr in start_dist:
                if start_dist[nbr] > start_dist[next_node] + 1:
                    start_dist[nbr] = min(start_dist[nbr], start_dist[next_node] + 1)
                    curr.append(nbr)
            else:
                start_dist[nbr] = start_dist[next_node] + 1
                curr.append(nbr)

    
    curr = [end]
    while curr:
        next_node = curr.pop(0)
        for nbr in get_neighbors(grid, next_node):
            if gat(grid, nbr) == "#":
                continue
            if nbr in end_dist:
                if end_dist[nbr] > end_dist[next_node] + 1:
                    end_dist[nbr] = min(end_dist[nbr], end_dist[next_node] + 1)
                    curr.append(nbr)
            else:
                end_dist[nbr] = end_dist[next_node] + 1
                curr.append(nbr)

    best_dist = start_dist[end]
    print(best_dist)

    for i,j in tqdm.tqdm(gridrange(grid)):
        pos = (j,i)
        if gat(grid, pos) == "#":
            continue
        for cheat in end_dist:
            d = abs(cheat[0] - pos[0]) + abs(cheat[1]-pos[1])
            if d > 20:
                continue

            if not in_grid(grid, cheat) or gat(grid, cheat) == "#":
                continue
            new_dist = start_dist[pos] + end_dist[cheat] + d
            if new_dist <= best_dist - 100:
                tot += 1
                # print(pos, cheat)


    print(tot)
    print(tot2)
    # break


# 811079 wrong

## almost made it to the leaderboard which was surprising to me, thought I was kind of slow today
## maybe people dropping off as it gets closer to Christmas
## one mistake: forgot to change the +2 I had hardcoded onto new_dist into a +d, otherwise pretty much went smoothly
## other small issue was my default linalg producing lists that didn't work with step (because lists aren't hashable), will fix
## runs in 9 seconds which is a little slow for AoC, but tolerable enough. Don't think it scales well though.
## probably could add some more grid utils like grabbing start/end if they're marked with S/E, getting Euclidean distance, etc.
## potentially even just the entire first part of building distances, since it's common enough for AoC walls to be "#"