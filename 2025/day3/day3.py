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

    def joltage(x):
        tens = max(x[:-1])
        ones = 0
        for i, y in enumerate(x):
            if y != tens:
                continue
            ones = max(x[i+1:])
            break
        return tens * 10 + ones
    
    for line in grid:
        tot += joltage(line)

    def joltage2(x, k):
        if k == 2:
            return joltage(x)
        max_digit = max(x[:-k+1])
        for i, y in enumerate(x):
            if y == max_digit:
                break
        return max_digit * 10 ** (k-1) + joltage2(x[i+1:], k-1)
    
    for line in grid:
        tot2 += joltage2(line, 12)

    print(tot)
    print(tot2)
    # break

# 6:26
# fairly straightforward, was a bit slow on figuring out finding the first entry matching the max value (which could have just been list.index())