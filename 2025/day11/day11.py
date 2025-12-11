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

    graph = {}
    for line in lines:
        key, vals = line.split(":")
        vals = vals.strip().split(" ")
        graph[key] = vals

    # start = "you"
    start = "svr"

    # prune to reachable
    reachable = set()
    reachable.add(start)
    curr = [start]
    while curr:
        c = curr.pop()
        if c in graph:
            for x in graph[c]:
                if x not in reachable and x not in curr:
                    curr.append(x)
                    reachable.add(x)
    graph = {x: y for x, y in graph.items() if x in reachable}

    reverse_graph = {}
    for key in reachable:
        reverse_graph[key] = [x for x, y in graph.items() if key in y]

    curr = {start: {(False, False): 1}}
    reached = set()
    reached.add(start)
    queue = [(start, False, False)]
    while queue:
        curr_label, has_fft, has_dac = queue.pop(0)
        is_leaf = True
        if curr_label not in reverse_graph:
            if len(queue) > 0:
                is_leaf = False
        else:
            for x in reverse_graph[curr_label]:
                if x in [y[0] for y in queue] or x not in curr:
                    is_leaf = False
        if not is_leaf:
            queue.append((curr_label, has_fft, has_dac))
            continue

        if curr_label not in graph:
            continue
        for dest in graph[curr_label]:
            next_has_fft = True if dest == "fft" else has_fft
            next_has_dac = True if dest == "dac" else has_dac
            
            if dest not in curr:
                curr[dest] = {}
            curr[dest][(next_has_fft, next_has_dac)] = curr.get(dest, {}).get((next_has_fft, next_has_dac), 0) + curr[curr_label][(has_fft, has_dac)]
            reached.add(dest)
            if (dest, next_has_fft, next_has_dac) not in queue:
                queue.append((dest, next_has_fft, next_has_dac))
    print(curr)
    tot2 = curr["out"][(True, True)]

    print(tot)
    print(tot2)
    # break

# 6422538818496 not right
# 139859314492667280 not right

# 41 mins
# kind of got confusing with the data structure, ended up needing to check the queue as well as the currently counted nodes
# a better structure probably checks all boolean tuples at a node, rather than adding them to the queue separately
# pruning to reachable was fairly important
