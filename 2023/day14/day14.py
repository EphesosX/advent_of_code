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
    grid = []
    for line in data:
        grid.append([x for x in line])
    
    rocks = []
    blocks = []
    m = len(grid)
    n = len(grid[0])
    for i in range(m):
        for j in range(n):
            if grid[i][j] == 'O':
                rocks.append((i,j))
            else:
                blocks.append((i,j))
    
    grid2 = [['.' if x == 'O' else x for x in y] for y in grid]
    new_rocks = []
    for i, j in rocks:
        while i > 0 and grid2[i-1][j] not in ['O', '#']:
            i -= 1
        grid2[i][j] = 'O'
        new_rocks.append((i,j))
    
    for i,j in new_rocks:
        tot += m - i

    def run_cycle(grid, rocks):
        # for x in grid:
        #     for y in x:
        #         print(y, end='')
        #     print()
        # print()
        for i, j in rocks:
            grid[i][j] = '.'
        
        new_rocks = []
        for i, j in sorted(rocks, key=lambda x: x[0]):
            while i > 0 and grid[i-1][j] not in ['O', '#']:
                i -= 1
            grid[i][j] = 'O'
            new_rocks.append((i,j))
        rocks = new_rocks
        # for x in grid:
        #     for y in x:
        #         print(y, end='')
        #     print()
        # print()
        for i, j in rocks:
            grid[i][j] = '.'
        
        new_rocks = [] # west
        for i, j in sorted(rocks, key=lambda x: x[1]):
            while j > 0 and grid[i][j-1] not in ['O', '#']:
                j -= 1
            grid[i][j] = 'O'
            new_rocks.append((i,j))
        rocks = new_rocks
        # for x in grid:
        #     for y in x:
        #         print(y, end='')
        #     print()
        # print()
        for i, j in rocks:
            grid[i][j] = '.'
        
        new_rocks = [] # south
        for i, j in sorted(rocks, key=lambda x: x[0], reverse=True):
            while i+1 < m and grid[i+1][j] not in ['O', '#']:
                i += 1
            grid[i][j] = 'O'
            new_rocks.append((i,j))
        rocks = new_rocks
        # for x in grid:
        #     for y in x:
        #         print(y, end='')
        #     print()
        # print()
        for i, j in rocks:
            grid[i][j] = '.'
        
        new_rocks = [] #east
        for i, j in sorted(rocks, key=lambda x: x[1], reverse=True):
            while j+1 < n and grid[i][j+1] not in ['O', '#']:
                j += 1
            grid[i][j] = 'O'
            new_rocks.append((i,j))
        rocks = new_rocks
        return grid, rocks

    old_grids = []
    new_grid = tuple(tuple(x for x in y) for y in grid)
    n_cycles = 0
    while new_grid not in old_grids:
        old_grids.append(new_grid)
        grid, rocks = run_cycle(grid, rocks)
        # print("#####################")
        n_cycles += 1
        new_grid = tuple(tuple(x for x in y) for y in grid)
        # for x in new_grid:
        #     print(x)

    for k, grid_i in enumerate(old_grids):
        if grid_i == new_grid:
            print(k)
    # for x in grid:
    #     for y in x:
    #         print(y, end='')
    #     print()
    # print()
    
    print('n cycles', n_cycles)
    for i in range((100000 - n_cycles) % 7 + 1):
        grid, rocks = run_cycle(grid, rocks)
    for i,j in rocks:
        tot2 += m - i

    

    print(tot)
    print(tot2)

    # 97242
    # 97246
    # 97240
    # 97248

    # 96064
    # 96061