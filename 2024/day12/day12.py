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

    regions = {}
    region_labels = {}
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            letter = grid[i][j]
            if letter not in regions:
                regions[letter] = {}
                regions[letter][(i,j)] = 0
                region_labels[letter] = [0]
            else:
                merge_regions = set()
                for pos in get_neighbors(grid, (i,j)):
                    if pos in regions[letter]:
                        merge_regions.add(regions[letter][pos])
                if len(merge_regions) == 0:
                    new_label = len(region_labels[letter])
                    regions[letter][(i,j)] = new_label
                    region_labels[letter].append(new_label)
                elif len(merge_regions) == 1:
                    regions[letter][(i,j)] = merge_regions.pop()
                else:
                    new_label = merge_regions.pop()
                    for pos in regions[letter]:
                        if regions[letter][pos] in merge_regions:
                            regions[letter][pos] = new_label
                    regions[letter][(i,j)] = new_label
    
    reverse_regions = {}
    for letter, letter_regions in regions.items():
        for pos, label in letter_regions.items():
            if (letter, label) not in reverse_regions:
                reverse_regions[(letter, label)] = set()
            reverse_regions[(letter, label)].add(pos)

    # print(regions)

    for ll, region in reverse_regions.items():
        per = 0
        sides = 0
        for pos in region:
            per += 4
            n_dirs = []
            e_dirs = []
            for nbr in get_neighbors(grid, pos, allow_empty=True):
                if in_grid(grid, nbr) and nbr in region:
                    per -= 1
                    n_dirs.append((nbr[0]-pos[0], nbr[1]-pos[1]))
                else:
                    sides += 1
                    e_dirs.append((nbr[0]-pos[0], nbr[1]-pos[1]))
            for dir in e_dirs:
                t_dir = turn(dir)
                if t_dir in n_dirs:
                    nbr = step(pos, t_dir)
                    nbr_nbr = step(nbr, dir)
                    if not in_grid(grid, nbr_nbr) or nbr_nbr not in region:
                        sides -= 1

        tot += per * len(region)
        tot2 += sides * len(region)

    print(tot)
    print(tot2)
    # break

## started a couple minutes late
## labeling the regions got a bit messy too since they needed to be kept distinct, but also multiple regions could merge together
## grid utilities really came in handy here, could probably have used even more of them like sub. Also should add a gridrange to loop over i,j for
## cases where the loops don't need separating
## messed up for a bit because my default get_neighbors didn't include locations outside of the grid, but those needed to be marked empty as well
