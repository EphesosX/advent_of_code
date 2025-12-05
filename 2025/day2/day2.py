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
    ranges_ = lines[0].split(",")
    ranges = [[x for x in range_.split("-")] for range_ in ranges_]

    print(ranges)

    for range_ in ranges:
        for y in range(int(range_[0]), int(range_[1])+1):
            valid = True
            z = str(y)
            for w in range(2, len(z)+1):
                if len(z) % w == 0:
                    invalid = True
                    m = len(z) // w
                    for k in range(w):
                        if z[:m] != z[k*m: k*m+m]:
                            invalid = False
                    if invalid:
                        valid = False
            if not valid:
                tot += y



    print(tot)
    print(tot2)
    # break

# 12:04
# ended up just brute forcing, could probably do something more clever since you only really need to iterate the first N digits of the range