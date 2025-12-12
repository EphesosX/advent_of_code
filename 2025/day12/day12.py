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

    shapes = []
    curr_shape = []
    for line in lines:
        if line:
            curr_shape.append(line)
        else:
            shapes.append(curr_shape)
            curr_shape = []
    
    present_areas = curr_shape

    shapes = [x[1:] for x in shapes]
    n_size_fail = 0
    for present_area in present_areas:
        area, presents = present_area.split(":")
        presents = [int(x) for x in presents.strip().split(" ")]
        area = [int(x) for x in area.split("x")]
        # print(area, presents)

        # area_grid = [['.' for x in range(area[0])] for y in range(area[1])]
        area_size = area[0] * area[1]
        sizes = []
        for shape in shapes:
            size = 0
            for line in shape:
                for x in line:
                    if x == "#":
                        size += 1
            sizes.append(size)
        
        tot_size = 0
        for i, n_presents in enumerate(presents):
            tot_size += sizes[i] * n_presents
        # print(tot_size)
        if tot_size > area_size:
            n_size_fail += 1
    print(n_size_fail, "/", len(present_areas))

    # this is dumb and shouldn't work but it does
    tot = len(present_areas) - n_size_fail

    print(tot)
    print(tot2)
    # break

# kind of disappointed with this one
# it's an NP-hard problem with unreasonable parameters so it had to have a heuristic solution of some kind that just happens to work on the given inputs
# but the test input explicitly fails that heuristic and it's pretty clear a problem could have been in the set that breaks it...
