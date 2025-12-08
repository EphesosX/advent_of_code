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

    positions = [tuple(int(x) for x in line.split(",")) for line in lines]

    n = 1000
    if filename == 'test_input.txt':
        n = 10

    def dist23d(pos1, pos2):
        return sum([((x-y)**2) for x, y in zip(pos1, pos2)])
    
    dists = []
    for i in range(len(positions)):
        pos = positions[i]
        for j in range(i+1, len(positions)):
            pos2 = positions[j]
            dists.append((dist23d(pos, pos2), i, j))

    dists = sorted(dists)
    # print(dists)

    import networkx as nx

    g = nx.Graph()
    for i in range(len(positions)):
        g.add_node(i)
    for i in range(n):
        g.add_edge(dists[i][1], dists[i][2])
    
    sizes = []
    for c in nx.connected_components(g):
        # print(c)
        sizes.append(len(c))
    
    sizes = sorted(sizes, reverse=True)
    print(sizes)
    tot = sizes[0] * sizes[1] * sizes[2]

    
    for i in range(n+1, len(dists)):
        g.add_edge(dists[i][1], dists[i][2])
        if nx.connected.is_connected(g):
            tot2 = positions[dists[i][1]][0] * positions[dists[i][2]][0]
            break


    print(tot)
    print(tot2)
    # break

# 15 minutes, very brute force, still took under a second though I could hear my fans spin up a bit
# connected components is linear time in the number of edges so overall this is O(E^2) where E is the number of edges required
# you could probably skip edges between already connected components to speed things up