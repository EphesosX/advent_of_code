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

    curr = 50
    for line in lines:
        zero_curr = (curr == 0)
        if line[0] == "L":
            curr -= int(line[1:])
            if curr < 0:
                if not zero_curr:
                    tot2 += (-curr) // 100 + 1
                else:
                    tot2 += (-curr) // 100
                curr %= 100
            elif curr == 0:
                tot2 += 1
            if curr == 0:
                tot += 1
                
        else:
            curr += int(line[1:])
            if curr >= 100:
                tot2 += curr // 100
                curr %= 100
            elif curr == 0:
                tot2 += 1
            if curr == 0:
                tot += 1

    print(tot)
    print(tot2)
    # break

# 4:19 part 1
# 2618 too low
# 5854 too low
# 18:02 part 2
# definitely not my proudest attempt, missed that you could go around multiple times
# also maybe should have chosen a different numbering scheme other than sticking to the one given? lots of awkwardness around tracking the current position

