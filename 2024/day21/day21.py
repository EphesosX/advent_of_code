import os
import re
import tqdm
import sys
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
from utils import *

from itertools import permutations

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

    dirmap = get_dir_map()
    loc = {'<': (0,0), 'v': (1,0), '>': (2,0), '^': (1,1), 'A': (2,1)} # key coords
    keyloc = {'0': (1,0), 'A': (2,0), '1': (0,1), '2': (1,1), '3': (2,1), '4': (0,2), '5': (1,2), '6': (2,2),'7': (0,3), '8': (1,3), '9': (2,3)}

    n_robots = 25 # number of directional keypad robots

    # to do a move on a robot, each robot does a sequence of moves ending in A
    # order of positions matters? 


    # given any vector on the dirpad, list all possible ways to travel that don't backtrack
    vec_paths = {}
    for dx in range(-2, 3):
        for dy in range(-3, 4):
            vec_paths[(dx, dy)] = set()
            moves = []
            if dx < 0:
                moves.append('<' * (-dx))
            else:
                moves.append('>' * dx)
            if dy < 0:
                moves.append('v' * (-dy))
            else:
                moves.append('^' * dy)
            for perm in permutations(moves):
                path = tuple([x for x in perm if x])
                path_str = ''
                for x in path:
                    path_str += x
                vec_paths[(dx, dy)].add(path_str)
    # issue: need to avoid gaps
    def get_paths(loc_dict, gap):
        paths = {}
        for start, start_loc in loc_dict.items():
            for end, end_loc in loc_dict.items():
                dxy = (end_loc[0]-start_loc[0], end_loc[1]-start_loc[1])
                paths[(start,end)] = []
                for path in vec_paths[dxy]:
                    curr_loc = start_loc
                    coord_path = []
                    for instr in path:
                        for key in instr:
                            dir_vec = dirmap[key]
                            curr_loc = add(curr_loc, dir_vec)
                            coord_path.append(curr_loc)
                    if curr_loc != end_loc:
                        print(start, end, path, coord_path, start_loc, end_loc)
                        raise Exception('Failed to reconstruct')
                    if gap not in coord_path:
                        paths[(start,end)].append(path)
        return paths

    dirpad_paths = get_paths(loc, (0,1))
    keypad_paths = get_paths(keyloc, (0,0))

    # cost of a path on pad n is the cost of executing each of its moves in sequence on pad n-1
    # cost('<<^A', n) = cost(path('A', '<')) + 1 + cost(path('<','^')) + cost(path('^','A'))
    # all paths assumed to end in A
    # can express things in terms of the cost of traveling between buttons


    costs = []
    costs.append({pair: 1 for pair in dirpad_paths}) # cost for the human to switch buttons is 0, plus one to press A
    for i in range(n_robots):
        new_cost = {}
        for pair, paths in dirpad_paths.items():
            path_costs = []
            for path in paths:
                cost = 0
                bookend_path = ['A']
                bookend_path.extend(path)
                bookend_path.append('A')
                for i in range(1, len(bookend_path)):
                    cost += costs[-1][(bookend_path[i-1], bookend_path[i])]

                path_costs.append(cost)

            new_cost[pair] = min(path_costs)
        costs.append(new_cost)

    def get_keypad_cost(digits):
        cost = 0
        for i in range(1, len(digits)):
            path_costs = []
            for path in keypad_paths[(digits[i-1], digits[i])]:
                path_cost = 0
                bookend_path = ['A']
                bookend_path.extend(path)
                bookend_path.append('A')
                for i in range(1, len(bookend_path)):
                    path_cost += costs[-1][(bookend_path[i-1], bookend_path[i])]
                path_costs.append(path_cost)
            cost += min(path_costs)
        return cost

    for line in lines:
        line_cost = get_keypad_cost('A'+line)
        tot += line_cost * int(line[:-1])

    print(tot)
    # break
    print(tot2)
    # break

## got stuck on this one and finally came back to it 11 months later (11-27-25)
## don't think I'm making the leaderboard...
## better late than never, figured I should finish the last advent calendar before starting 2025's
## did part 1 the first time (last December) via a brute force computation of all paths
## tried something similar to this but got stuck for several hours and gave up, coming back to it with a fresh mind and a good idea of the approach helped
## as did realizing that the only costs needed were the cost to move from location X to location Y and press button Y
