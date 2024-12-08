import os
import re
import tqdm
from math import gcd

basepath = os.path.dirname(os.path.abspath(__file__))

def step(pos, dir):
    return (pos[0] + dir[0], pos[1]+dir[1])

def in_grid(grid, pos):
    return pos[0] >= 0 and pos[0] < len(grid) and pos[1] >= 0 and pos[1] < len(grid[pos[0]])

for filename in ['test_input.txt', 'input.txt']:
    print(filename)
    tot = 0
    tot2 = 0

    lines = []
    with open(os.path.join(basepath, filename), 'r') as fin:
        lines = [[y for y in x.strip()] for x in fin]
    antennas = set()
    for x in lines:
        for y in x:
            antennas.add(y)
    antennas = [x for x in antennas if x != "."]
    print(antennas)
    m = len(lines)
    n = len(lines[0])

    antenna_locs = {antenna: [] for antenna in antennas}
    for i in range(len(lines)):
        line = lines[i]
        for j in range(len(line)):
            if line[j] in antenna_locs:
                antenna_locs[line[j]].append((i,j))

    # print(antenna_locs)

    antinodes = set()
    for antenna, locs in antenna_locs.items():
        for loc1 in locs:
            for loc2 in locs:
                if loc1 != loc2:
                    for antinode in [(2 * loc2[0] - loc1[0], 2*loc2[1]-loc1[1]), (2 * loc1[0] - loc2[0], 2*loc1[1]-loc2[1])]:
                        if in_grid(lines, antinode):
                            antinodes.add(antinode)

    tot = len(antinodes)
    # for i, j in antinodes:
    #     lines[i][j] = "#"
    # for line in lines:
    #     print(line)
    print(tot)
    
    antinodes = set()
    for antenna, locs in antenna_locs.items():
        for loc1 in locs:
            for loc2 in locs:
                if loc1 != loc2:
                    dir = (loc1[0]-loc2[0], loc1[1]-loc2[1])
                    div = gcd(dir[0], dir[1])
                    dir = (dir[0] // div, dir[1] // div)
                    pos = loc1
                    while in_grid(lines, pos):
                        antinodes.add(pos)
                        pos = step(pos, dir)
                    pos = loc1
                    dir = (-dir[0], -dir[1])
                    while in_grid(lines, pos):
                        antinodes.add(pos)
                        pos = step(pos, dir)
                
    tot2 = len(antinodes)
    print(tot2)
    # break

## I should probably just have a general utils import for vector math, or use numpy or something
## much faster to write 2*x-y than (2*x[0]-y[0],2*x[1]-y[1])
