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

    digits = lines[0]

    i = 0
    id = 0
    blocks = {}
    spaces = {}
    curr = 0
    while i < len(digits):
        block_size = int(digits[i])
        blocks[i] = (id, block_size, curr)
        i += 1
        curr += block_size
        id += 1
        if i < len(digits):
            space_size = int(digits[i])
            spaces[i] = (space_size, curr)
            curr += space_size
            i += 1
    
    j = max(x for x in spaces)
    max_block = max([idx for idx in blocks if idx < j])
    def block_sum():
        return sum([x[1] for idx, x in blocks.items() if idx > max_block])
    def space_sum():
        return sum([x[0] for i, x in spaces.items() if i < j])
    while block_sum() < space_sum():
        j -= 2
        max_block = max([idx for idx in blocks if idx < j])
    print(block_sum(), space_sum())
    print(j)
    
    print(max_block)
    curr = 0
    curr_idx = 0
    curr_reverse_idx = max([x for x in blocks])
    curr_reverse_remainder = [x[1] for idx, x in blocks.items() if idx == curr_reverse_idx][0]
    # fs = ""
    while curr_idx <= max_block:
        # print("curr_idx", curr_idx)
        for i, block in blocks.items():
            id, block_size, loc = block
            if curr_idx == i:
                tot += id * sum([x for x in range(curr, curr+block_size)])
                # print("block", i, id, block_size, tot)
                # fs += str(id) * block_size
                curr += block_size
        for i, space in spaces.items():
            space_size, loc = space
            if curr_idx == i:
                n_moved = 0
                while n_moved < space_size:
                    n_to_move = min(curr_reverse_remainder, space_size - n_moved)
                    curr_reverse_remainder -= n_to_move
                    n_moved += n_to_move
                    # print("Moving ", n_to_move)
                    id = blocks[curr_reverse_idx][0]
                    tot += id * sum([x for x in range(curr, curr+n_to_move)])
                    # print("Space", i, id, space_size, tot)
                    # fs += str(id) * n_to_move
                    curr += n_to_move
                    if curr_reverse_remainder == 0:
                        curr_reverse_idx -= 2
                        curr_reverse_remainder = blocks[curr_reverse_idx][1]
        curr_idx += 1

    print(max_block, curr_reverse_idx)
    id = blocks[curr_reverse_idx][0]
    tot += id * sum([x for x in range(curr, curr+curr_reverse_remainder)])
    curr += curr_reverse_remainder
    print(curr, sum([x[1] for x in blocks.values()]))
    # fs += str(id) * curr_reverse_remainder

    # print(fs)

    print(tot)

    curr = 0
    fs = ""
    for i in sorted(blocks.keys(), reverse=True):
        id, block_size, loc = blocks[i]
        for j in sorted(spaces.keys()):
            if j > i:
                break
            space_size, space_loc = spaces[j]
            if space_size >= block_size:
                blocks[i] = (id, block_size, space_loc)
                if space_size == block_size:
                    del spaces[j]
                else:
                    spaces[j] = (space_size - block_size, space_loc + block_size)
                
                new_idx = i
                new_size = block_size
                new_loc = loc
                k = i + 1
                while k not in blocks and k <= max(spaces.keys()):
                    if k in spaces:
                        new_size += spaces[k][0]
                        del spaces[k]
                    k += 1

                k = i - 1
                while k not in blocks and k >= min(spaces.keys()):
                    if k in spaces:
                        new_idx = k
                        new_size += spaces[k][0]
                        new_loc = spaces[k][1]
                        del spaces[k]
                    k -= 1
                spaces[new_idx] = (new_size, new_loc)
                break


        # if i in blocks:
        #     id, block_size = blocks[i]
        #     tot += id * sum([x for x in range(curr, curr+block_size)])
        #     curr += block_size
        #     fs += str(id) * block_size
        #     del blocks[i]
        # elif i in spaces:
        #     to_move = spaces[i]
        #     del spaces[i]
        #     j = max([x for x in blocks])
        #     while j >= 0 and to_move > 0:
        #         if j not in blocks:
        #             j -= 1
        #             continue
        #         id, block_size = blocks[j]
        #         if block_size <= to_move:
        #             print("move ", id, block_size)
        #             to_move -= block_size
        #             tot += id * sum([x for x in range(curr, curr+block_size)])
        #             curr += block_size
        #             fs += str(id) * block_size
        #             del blocks[j]
                    
        #             # combine with other spaces
        #             new_idx = j
        #             new_size = block_size
        #             k = j + 1
        #             while k not in blocks and k <= max(spaces.keys()):
        #                 if k in spaces:
        #                     new_size += spaces[k]
        #                     del spaces[k]
        #                 k += 1
        #                 print(k)

        #             k = j - 1
        #             while k not in blocks and k >= min(spaces.keys()):
        #                 if k in spaces:
        #                     new_idx = k
        #                     new_size += spaces[k]
        #                 k -= 1
        #             spaces[new_idx] = new_size
        #             print(new_idx, new_size)
        #             print(spaces)
        #             break
        #         j -= 1
        #     curr += to_move
        #     fs += "." * to_move
        # if len(blocks) == 0:
        #     break

    for i, block in blocks.items():
        id, block_size, loc = block
        tot2 += id * sum([x for x in range(loc, loc+block_size)])
    # print(fs)

    print(tot2)
    # break

# 6199567561933 wrong

## This one was a bit rough for me, went in with completely wrong data structures that I had to revise a lot
## Originally I just had a list of tuples of (id, size), then it had to be (idx, id, size), then a dict from idx to (id, size), and finally I had to store the position too for part 2
## Also very messy with indexing for various fields, probably should have just taken the time to create an object
## Also messed up the order of moving blocks the first time, thought I had to fill spaces from left to right instead of moving blocks into spaces from right to left
