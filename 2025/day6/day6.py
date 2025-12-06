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
        lines = [x for x in fin]
        grid = [[x for x in line.split()] for line in lines]

    ops = grid[-1]
    grid = grid[:-1]

    for i in range(len(grid[0])):
        curr = None
        for j in range(len(grid)):
            if curr is None:
                curr = int(grid[j][i])
            else:
                if ops[i] == "*":
                    curr *= int(grid[j][i])
                elif ops[i] == "+":
                    curr += int(grid[j][i])
        tot += curr

    
    ops = []
    for i, op in enumerate(lines[-1]):
        if op != ' ' and op != '\n':
            ops.append((i,op))
    
    for j in range(len(ops)):
        k = max([len(x) for x in lines]) - 1
        if j < len(ops) - 1:
            print(ops[j+1])
            k = ops[j+1][0]-1
        i, op = ops[j]
        c = [0] * (k-i)
        # print(c)
        # print(i, k)
        for p in range(len(lines) - 1):
            for m in range(i, k):
                x = lines[p][m]
                if x != ' ' and x != "\n":
                    c[m-i] *= 10
                    # print(p, m, x)
                    c[m-i] += int(x)
    
        print(c)

        curr = c[0]
        for x in range(1, len(c)):
            if op == "*":
                curr *= c[x]
            elif op == "+":
                curr += c[x]
        tot2 += curr

                    
            

    print(tot)
    print(tot2)
    # break

# got distracted in the middle, probably spent around 20 minutes?
# forgot that my default strip removed leading spaces, and then had to deal with newlines awkwardly