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


    patterns = lines[0].strip().split(", ")
    towels = lines[2:]
    for towel in towels:
        towel = towel.strip()
        valid = []
        counts = {"": 1}
        curr_combos = [(0,"")]
        while curr_combos:
            curr_len, curr = curr_combos.pop(0)
            for pattern in patterns:
                if towel[len(curr):len(curr)+len(pattern)] != pattern:
                    continue
                new_curr = curr+pattern
                if new_curr in counts:
                    # print('O:', new_curr, counts[curr], counts[new_curr])
                    counts[new_curr] += counts[curr]
                else:
                    # print('N:', new_curr, counts[curr])
                    counts[new_curr] = counts[curr]
                    bisect.insort(curr_combos, (len(new_curr), new_curr))
        if counts.get(towel,0) > 0:
            tot += 1
        tot2 += counts.get(towel,0)

    print(tot)
    print(tot2)
    # break

## Easy day, but super fast times to compete with
## Figured from the start that part 2 would be counting all combos, but my solution of just trying all of them scaled poorly
## realized I'd need to do dynamic programming and save the counts
## then my only big mistake was leaving in some old code I had to cut off the count early (which I knew I'd have to get rid of when writing it, I just forgot to actually get rid of it...)
