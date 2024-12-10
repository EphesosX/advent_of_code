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
        grid = [[int(x) for x in line] for line in lines]

    trail_locs = [[set() for x in y] for y in grid]
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            d = grid[i][j]
            if d == 9:
                trail_locs[i][j].add((i,j))
            
    
    for m in range(9)[::-1]:
        for i in range(len(grid)):
            for j in range(len(grid[i])):
                d = grid[i][j]
                if d == m:
                    for nbr_i, nbr_j in get_neighbors(grid, (i,j)):
                        if in_grid(grid, (nbr_i,nbr_j)) and grid[nbr_i][nbr_j] == d+1:
                            trail_locs[i][j] = trail_locs[i][j].union(trail_locs[nbr_i][nbr_j])

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            d = grid[i][j]
            if d == 0:
                tot += len(trail_locs[i][j])

    # for i in range(len(grid)):
    #     line = ""
    #     for j in range(len(grid[i])):
    #         d = grid[i][j]
    #         line += f"{len(trail_locs[i][j]):3}"
    #     print(line)


    print(tot)
    print(tot2)
    # break

# 256 wrong... or was it?
# Accidentally read the problem wrong and ended up doing part 2 first
# Arguably simpler because you only need to track a single digit per grid location, and not the set of all 9's led to from that location
# Left my code as the part 1 solution since I wrote over the part 2, just scrolled back in my log and grabbed the output