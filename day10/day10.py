import os
basepath = os.path.dirname(os.path.abspath(__file__))

def get_neighbors(grid, token, i, j, m, n):
    nbrs = []
    if token in ['S', 'L', 'J', '|']:
        if i > 0:
            if grid[i-1][j] in ['S','F','7', '|']:
                nbrs.append((i-1,j))
    if token in ['S', '7', 'F', '|']:
        if i < m-1:
            if grid[i+1][j] in ['S','L','J', '|']:
                nbrs.append((i+1,j))
    if token in ['S', '7', 'J', '-']:
        if j > 0:
            if grid[i][j-1] in ['S','L','F', '-']:
                nbrs.append((i,j -1))
    if token in ['S', 'L', 'F', '-']:
        if j < n-1:
            if grid[i][j+1] in ['S','7','J', '-']:
                nbrs.append((i,j +1))
    return nbrs

def get_neighbors2(i, j, m, n):
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

for filename in ['test_input.txt', 'input.txt']:
    print(filename)
    data = []

    with open(os.path.join(basepath, filename), 'r') as fin:
        for line in fin:
            data.append(line.strip())


    tot = 0
    tot2 = 0
    grid = []
    for line in data:
        grid.append([x for x in line])
    m = len(grid)
    n = len(grid[0])
    
    start = None
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == 'S':
                start = (i, j)

    curr = [start]
    dist = [[0] * len(grid[0]) for y in range(len(grid))]
    dist[start[0]][start[1]] = 1
    while curr:
        i, j = curr.pop()
        for x, y in get_neighbors(grid, grid[i][j], i, j, len(grid), len(grid[i])):
            if grid[x][y] == ".":
                continue
            if dist[x][y] == 0:
                curr.append((x,y))
                dist[x][y] = dist[i][j] + 1
            else:
                if dist[x][y] >= dist[i][j] + 1:
                    curr.append((x,y))
                    dist[x][y] = min(dist[x][y], dist[i][j] + 1)
    print(max([max(x) for x in dist]) - 1)
    
    in_loop = [[dist[i][j] == 0 for j in range(len(grid[i]))] for i in range(len(grid))]
    
    
    curr2 = [start]
    dist2 = [[0] * len(grid[0]) for y in range(len(grid))]
    dist2[start[0]][start[1]] = 1
    big_grid = [[False for j in range(2*n)] for i in range(2*m)]
    big_grid[start[0] * 2][start[1]*2] = True
    while curr2:
        i, j = curr2.pop()
        for x, y in get_neighbors(grid, grid[i][j], i, j, len(grid), len(grid[i])):
            if grid[x][y] == ".":
                continue
            if dist2[x][y] == 0:
                curr2.append((x,y))
                dist2[x][y] = dist2[i][j] + 1
                big_grid[2*x][2*y] = True
                big_grid[(x+i)][(y+j)] = True
            if grid[x][y] == 'S':
                big_grid[(x+i)][(y+j)] = True
            if grid[i][j] == 'S':
                break
    
    # for x in dist:
    #     for y in x:
    #         print(1 if y!=0 else 0, end='')
    #     print()

    # for x in big_grid:
    #     for y in x:
    #         print("." if y else "#", end='')
    #     print()
    # print()

    in_loop2 = [[not big_grid[i][j] for j in range(len(big_grid[i]))] for i in range(len(big_grid))]
    # for x in in_loop2:
    #     for y in x:
    #         print('.' if y else '#', end='')
    #     print()
    
    curr3 = []
    for i in [0, 2*m-1]:
        for j in range(2*n):
            if in_loop2[i][j]:
                curr3.append((i,j))
                in_loop2[i][j] = False
    for i in range(2*m):
        for j in [0, 2*n-1]:
            if in_loop2[i][j]:
                curr3.append((i,j))
                in_loop2[i][j] = False

    # for i in range(2*m):
    #     for j in range(2*n):
    #         print("." if (i,j) in curr3 else "#", end='')
    #     print()
    # for x in in_loop2:
    #     for y in x:
    #         print('.' if y else '#', end='')
    #     print()

    
    while curr3:
        curr4 = []
        for i, j in curr3:
        # i, j = curr3.pop()
            for x, y in get_neighbors2(i, j, 2*m, 2*n):
                if not in_loop2[x][y]:
                    continue
                in_loop2[x][y] = False
                curr4.append((x,y))
        # for i in range(2*m):
        #     for j in range(2*n):
        #         print('.' if in_loop2[i][j] else '#' if (i, j) not in curr4 else 'X', end='')
        #     print()
        curr3 = curr4
        # input()

        
    
    print(sum([sum([1 if in_loop2[2*i][2*j] else 0 for j in range(len(grid[i]))]) for i in range(m)]))
    # for x in in_loop2:
    #     for y in x:
    #         print("." if y else "#", end='')
    #     print()
    # break

    print(tot2)
