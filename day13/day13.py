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

for filename in ['test_input.txt', 'input.txt']:
    print(filename)
    data = []

    with open(os.path.join(basepath, filename), 'r') as fin:
        for line in fin:
            data.append(line.strip())

    tot = 0
    tot2 = 0
    grids = []
    grid = []
    for line in data:
        if line:
            grid.append(line)
        else:
            grids.append(grid)
            grid = []
    if grid:
        grids.append(grid)

    for grid in grids:
        m = len(grid)
        n = len(grid[0])
        for i in range(m-1):
            is_reflect = True
            smudges = 0
            for i2 in range(i+1):
                if i+i2+1 >= m:
                    break
                for j in range(n):
                    if grid[i+i2+1][j] != grid[i-i2][j]:
                        smudges += 1
                        if smudges > 1:
                            is_reflect = False
                            break
            if is_reflect and smudges == 1:
                tot += (i+1) * 100
                # for x in grid:
                #     for y in x:
                #         print(y, end='')
                #     print()
                # print('i', i+1)
        for j in range(n-1):
            is_reflect = True
            smudges = 0
            for j2 in range(j+1):
                if j+j2+1 >= n:
                    break
                for i in range(m):
                    if grid[i][j+j2+1] != grid[i][j-j2]:
                        smudges += 1
                        if smudges > 1:
                            is_reflect = False
                            break
            if is_reflect and smudges == 1:
                tot += (j+1)
                # for x in grid:
                #     for y in x:
                #         print(y, end='')
                #     print()
                # print('j', j+1)

    print(tot)
    print(tot2)
    # 25747