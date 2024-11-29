import os
import networkx as nx

basepath = os.path.dirname(os.path.abspath(__file__))

def get_neighbors(i, j, m, n):
    nbrs = []
    if i > 0:
        nbrs.append((i-1,j))
    if i < m-1:
        nbrs.append((i+1,j))
    if j > 0:
        nbrs.append((i,j-1))
    if j < n-1:
        nbrs.append((i,j+1))
    return nbrs

def print_grid(grid):
    print(stringify_grid(grid))

def stringify_grid(grid):
    s = ""
    for x in grid:
        for y in x:
            s += y if y is not None else '_'
        s += "\n"
    s += "\n"
    return s

dir_map = {'U': (-1,0), 'D': (1,0), 'L':(0,-1), 'R': (0,1)}


for filename in ['test_input.txt', 'input.txt']:
    print(filename)
    data = []

    with open(os.path.join(basepath, filename), 'r') as fin:
        for line in fin:
            data.append(line.strip())

    tot = 0
    tot2 = 0
    graph = {}
    edges = []
    for line in data:
        src = line.split(":")[0]
        dsts = line.split(":")[1].strip().split()
        graph[src] = dsts
        edges.extend([(src, dst) for dst in dsts])
    
    g = nx.DiGraph(edges)
    
    for comm in nx.community.girvan_newman(g):
        print(comm)
        print(len(comm[0]) * len(comm[1]))
        break

    print(tot)
    print(tot2)
