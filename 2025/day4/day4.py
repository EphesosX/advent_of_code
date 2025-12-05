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

    for i, j in gridrange(grid):
        n = 0
        if gat(grid, (i,j)) != "@":
            continue
        for i2 in range(i-1, i+2):
            for j2 in range(j-1, j+2):
                if in_grid(grid, (i2, j2)):
                    if gat(grid, (i2,j2)) == "@":
                        n += 1

        if n < 5:
            tot += 1

    removed = True
    while removed:
        removed = False
        for i, j in gridrange(grid):
            n = 0
            if gat(grid, (i,j)) != "@":
                continue
            for i2 in range(i-1, i+2):
                for j2 in range(j-1, j+2):
                    if in_grid(grid, (i2, j2)):
                        if gat(grid, (i2,j2)) == "@":
                            n += 1

            if n < 5:
                tot2 += 1
                grid[j][i] = 'x'
                removed = True
        # print_grid(grid)
        # input()

    print(tot)
    print(tot2)
    # break

# 6:53
# having grid helpers was nice, but I forgot which order I did the indices in and was trying to set grid[i][j] instead of grid[j][i]
# also my grid helper for the neighborhood didn't support diagonals so I had to remake it, and my quick one accidentally included the center which I didn't expect
# should probably make a habit of naming (i,j) as pos rather than retyping it all the time