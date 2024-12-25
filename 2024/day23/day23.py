import os
import re
import tqdm
import sys
import networkx as nx
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

    graph = nx.Graph()
    for line in lines:
        a, b = line.split("-")
        graph.add_edge(a, b)

    for clique in nx.enumerate_all_cliques(graph):
        if len(clique) == 3:
            for node in clique:
                if 't' == node[0]:
                    # print(clique)
                    tot += 1
                    break
        elif len(clique) > 3:
            break

    print(tot)
    # print(nx.approximation.max_clique(graph))
    # tot2 = len(nx.approximation.max_clique(graph))
    max_clique = max(nx.find_cliques(graph), key=len)
    print(max_clique)
    tot2 = len(max_clique)
    print(tot2)
    print(','.join(sorted(max_clique)))
    # break

# 2660 too high
## because I forgot that nodes need to start with 't', not just have 't' in them...
# acedfhkdlfmbompeqtuouyvrwg wrong
## because I didn't join with commas...

## fairly straightforward, if you have networkx installed
## for some reason approximate max clique didn't work for me on the test input, so I just brute forced on all cliques
