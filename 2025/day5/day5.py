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
        # grid = [[x for x in line] for line in lines]

    id_ranges = []
    ids = []
    for line in lines:
        if '-' in line:
            id_ranges.append(tuple([int(x) for x in line.split('-')]))
        else:
            if line:
                ids.append(int(line))

    for id in ids:
        for id_range in id_ranges:
            if id >= id_range[0] and id <= id_range[1]:
                tot += 1
                break
    
    def overlap(r1, r2):
        if r1[0] <= r2[0] and r1[1] >= r2[0]:
            return True
        if r1[0] > r2[0] and r1[0] <= r2[1]:
            return True
        return False

    merged = True
    while merged:
        merged = False
        id_ranges_copy = [x for x in id_ranges]
        for i, id_range in enumerate(id_ranges):
            for j, id_range2 in enumerate(id_ranges):
                if j <= i:
                    continue
                if overlap(id_range, id_range2):
                    del id_ranges_copy[j]
                    del id_ranges_copy[i]
                    id_ranges_copy.append((min(id_range[0], id_range2[0]), max(id_range[1], id_range2[1])))
                    merged = True
                    break
                    
            if merged:
                break
        if merged:
            id_ranges = id_ranges_copy

    for id_range in id_ranges:
        tot2 += id_range[1] - id_range[0] + 1

    print(tot)
    print(tot2)
    # break

# 19:09, started 2 minutes late
# having something named 'range' while also needing the range() function is annoying
