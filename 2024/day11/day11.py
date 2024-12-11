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
    nums = [int(x) for x in lines[0].split(" ")]

    for i in range(25):
        new_nums = []
        for num in nums:
            if num == 0:
                new_nums.append(1)
            elif len(str(num)) % 2 == 0:
                num_str = str(num)
                new_nums.append(int(num_str[:len(num_str)//2]))
                new_nums.append(int(num_str[len(num_str)//2:])) 
            else:
                new_nums.append(num * 2024)
        nums = new_nums
    tot = len(new_nums)

    print(tot)

    nums = [int(x) for x in lines[0].split(" ")]
    len_cache = {}
    def compute(num, remaining):
        # print(num, remaining)
        # input()
        if remaining == 0:
            return 1
        if (num, remaining) in len_cache:
            return len_cache[(num, remaining)]
        # print(remaining)
        # input()
        newlen = None
        if num == 0:
            newlen = compute(1, remaining-1)
        elif len(str(num)) % 2 == 0:
            num_str = str(num)
            newlen = compute(int(num_str[:len(num_str)//2]), remaining-1) + compute(int(num_str[len(num_str)//2:]), remaining-1)
        else:
            newlen = compute(num * 2024, remaining-1)
        # print(num, len(len_cache[num]), remaining)
        len_cache[(num, remaining)] = newlen
        return len_cache[(num, remaining)]

    tot = 0
    for num in nums:
        compute(num, 75)
        # tot += len_cache[(num, 25)]
        tot2 += len_cache[(num, 75)]
    # print(len_cache)

    # print(len_cache[0])
    # print(len_cache[(0, 25)])

    print(tot)
    print(tot2)
    # break

## did okay on part 1 but messed up on part 2, didn't notice that nums got altered by my part 1 code so I was getting huge results
## spent most of my time thinking my caching approach was wrong and redoing it over and over