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
    robots = []
    with open(os.path.join(basepath, filename), 'r') as fin:
        lines = [x.strip() for x in fin]
        grid = [[x for x in line] for line in lines]

    for line in lines:
        pos = line.split("p=")[-1].split(" v=")[0]
        pos = [int(x) for x in pos.split(",")]
        vel = line.split("v=")[-1].strip()
        vel = [int(x) for x in vel.split(",")]
        robots.append((pos, vel))

    n = 103
    m = 101
    if filename[0] == 't':
        n = 7
        m = 11
    
    grid = [[0 for x in range(n)] for y in range(m)]
    quads = [[0,0,0],[0,0,0],[0,0,0]]
    for robot in robots:
        pos, vel = robot
        x,y = add(mul(vel, 100), pos)
        i = 0 if x % m < m//2 else 1 if x % m > m // 2 else 2
        j = 0 if y % n < n//2 else 1 if y % n > n // 2 else 2
        quads[i][j] += 1
        # print(x%m, y%n)
        grid[x%m][y%n] += 1
    
    print(quads)
    tot = quads[0][0] * quads[0][1] * quads[1][0] * quads[1][1]


    if filename[0] != "t":
        for step in range(1, 1000000):
            grid = [[0 for x in range(n)] for y in range(m)]
            for robot in robots:
                pos, vel = robot
                x,y = add(mul(vel, step), pos)
                grid[x%m][y%n] += 1
            tree = True
            for line in grid:
                for d in line:
                    if d > 1:
                        tree = False
            if not tree:
                continue
            print(step)
            for line in grid:
                l = ""
                for d in line:
                    l += str(d) if d else " "

                print(l)
            input()
    print(tot)
    print(tot2)
    # break


# 232832880 wrong

## Got x and y confused for part 1, had it solved in like 10 minutes except for that
## Part 2 was mostly about realizing that probably the tree was going to be made up only of 1's, took a bit of guessing around though
## thought maybe it'd happen in the first 10 or so and I could just check each image one by one