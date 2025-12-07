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

    curr = set()
    for i in range(len(lines[0])):
        if lines[0][i] == "S":
            curr.add(i)
    
    for i in range(1, len(lines)):
        new_curr = set()
        for j, c in enumerate(lines[i]):
            if c == "^" and j in curr:
                new_curr.add(j-1)
                new_curr.add(j+1)
                tot += 1
            elif j in curr:
                new_curr.add(j)
        curr = new_curr
    
    curr = {}
    for i in range(len(lines[0])):
        if lines[0][i] == "S":
            curr[i] = 1
    
    for i in range(1, len(lines)):
        new_curr = {}
        for j, c in enumerate(lines[i]):
            if c == "^" and j in curr:
                new_curr[j-1] = new_curr.get(j-1, 0) + curr[j]
                new_curr[j+1] = new_curr.get(j+1, 0) + curr[j]
            elif j in curr:
                new_curr[j] = new_curr.get(j,0) + curr[j]
        curr = new_curr
    tot2 = sum(curr.values())

    print(tot)
    print(tot2)
    # break

# 1689 wrong

# 9 minutes, started a minute late
# messed up the first part by forgetting the elif condition the first time
# vaguely remembered doing "count the number of paths" problems before so setting up the dictionary was pretty simple
# probably could have used a defaultdict to avoid typing get(x,0) all the time
