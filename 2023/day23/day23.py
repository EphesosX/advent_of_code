import os
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
    
    grid = []
    for line in data:
        grid.append([x for x in line])
    m = len(grid)
    n = len(grid[0])
    print(m,n)
    for j in range(n):
        if grid[0][j] == '.':
            start = (0, j)
            break

    tot = 0
    tot2 = 0

    # hikes = [(start, )]
    # ended_hikes = []
    allowed_steps = {'>': (0,1), '<': (0,-1), '^': (-1,0), 'v': (1,0)}
    # while hikes:
    #     hike = hikes.pop()
    #     print(len(hikes), len(hike))
    #     for nbr in get_neighbors(*hike[-1], m, n):
    #         if nbr in hike:
    #             continue
    #         if grid[nbr[0]][nbr[1]] != "#":
    #             last_char = grid[hike[-1][0]][hike[-1][1]]
    #             if last_char in ['>', '<', '^', 'v']:
    #                 if (nbr[0] - hike[-1][0], nbr[1]-hike[-1][1]) != allowed_steps[last_char]:
    #                     continue
    #             if nbr[0] == m-1:
    #                 ended_hikes.append(len(hike))
    #             else:
    #                 hikes.append(tuple([x for x in hike] + [nbr]))

    # print(ended_hikes)
    # tot = max(ended_hikes)
    # print(tot)
    
    hikes = [(start, )]
    ended_hikes = []
    visited = set()
    end = None
    while hikes:
        hike = hikes.pop()
        n_adj = 0
        for nbr in get_neighbors(*hike[-1], m, n):
            if len(hike) > 1 and nbr == hike[-2]:
                continue
            if nbr in visited or nbr in hike:
                n_adj += 1
                ended_hikes.append(tuple([x for x in hike] + [nbr]))
                continue
            if grid[nbr[0]][nbr[1]] != "#":
                last_char = grid[hike[-1][0]][hike[-1][1]]
                # if last_char in ['>', '<', '^', 'v']:
                #     if (nbr[0] - hike[-1][0], nbr[1]-hike[-1][1]) != allowed_steps[last_char]:
                #         continue
                if nbr[0] == m-1:
                    ended_hikes.append([x for x in hike] + [nbr])
                    end = nbr
                    visited.add(nbr)
                else:
                    hikes.append(tuple([x for x in hike] + [nbr]))
                n_adj += 1
        if n_adj > 1:
            visited.add(hike[-1])
            # print(len(hikes))
            # print(visited)
            # input()

    edges = set()
    for hike in ended_hikes:
        curr = start
        n_steps = 1
        for x in hike[1:]:
            if x in visited:
                edges.add((curr, x, n_steps))
                n_steps = 0
                curr = x
            n_steps += 1
    # for edge in edges:
    #     print(edge)

    import networkx as nx
    g = nx.Graph()
    for src, dst, weight in edges:
        g.add_edge(str(src), str(dst), weight=weight)

    path_lengths = []
    for path in nx.all_simple_edge_paths(g, str(start), str(end)):
        path_length = 0
        for edge in path:
            path_length += g.get_edge_data(*edge)["weight"]
        path_lengths.append(path_length)
    tot2 = max(path_lengths)
    print(tot2)

    missing = []
    for i in range(m):
        for j in range(n):
            if grid[i][j] != "#":
                found = False
                for hike in ended_hikes:
                    if (i,j) in hike:
                        found = True
                        break
                if not found:
                    missing.append((i,j))
    print(len(missing))

    if missing:
        for i in range(m):
            for j in range(n):
                if (i,j) in missing:
                    print('*', end='')
                else:
                    print('.', end='')
            print()
    # 5770 wrong
    # 6442