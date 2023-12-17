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
        grid.append([int(x) for x in line])

    def print_grid(grid):
        for x in grid:
            for y in x:
                print(y if y is not None else '_', end=',')
            print()
        print()
    
    m = len(grid)
    n = len(grid[0]) if grid else 0
    print(m, n)
    for i in range(m):
        for j in range(n):
            pass

    curr = [(0,0,0,1,1,0), (0,0,1,0,1,0)]
    min_cost = {}
    min_costs = [[None for y in x] for x in grid]
    min_cost_to_target = [[None for y in x] for x in grid]
    min_cost_to_target[m-1][n-1] = 0
    for l in range(1, m+n):
        for dy in range(l+1):
            dx = l - dy
            y = m-1 - dy
            x = n-1 - dx
            if y < 0 or x < 0:
                continue
            costs = []
            if y < m-1:
                costs.append(min_cost_to_target[y+1][x] + grid[y+1][x])
            if x < n-1:
                costs.append(min_cost_to_target[y][x+1] + grid[y][x+1])
            min_cost_to_target[y][x] = min(costs)

    target_min = None
    while curr:
        y, x, dy, dx, l, c = curr.pop()

        y += dy
        x += dx
        if x < 0 or x >= n or y < 0 or y >= m:
            continue
        c += grid[y][x]
        best_c = c + min_cost_to_target[y][x]
        if target_min is not None and best_c >= target_min:
            continue
        if y == m-1 and x == n-1:
            if target_min is None:
                target_min = c
            else:
                target_min = min(target_min, c)
                print(target_min, len(curr))
            continue
        if (y, x, dy, dx) in min_cost:
            better = False
            for l2, c2 in min_cost[(y,x,dy,dx)].items():
                if c2 <= c and l2 <= l and l2 >= 4:
                    better = True
            if better:
                continue
        else:
            min_cost[(y, x, dy, dx)] = {}
        min_cost[(y, x, dy, dx)][l] = c
        # min_costs[y][x] = c if min_costs[y][x] is None else min(min_costs[y][x], c)

        # left right straight
        if dx + dy > 0:
            if l >= 4:
                curr.append((y,x,-dx,-dy,1,c))
                curr.append((y,x,dx,dy,1,c))
            # if l < 3:
            if l < 10:
                curr.append((y,x,dy,dx,l+1,c))
        else:
            if l >= 4:
                curr.append((y,x,dx,dy,1,c))
            # if l < 3:
            if l < 10:
                curr.append((y,x,dy,dx,l+1,c))
            if l >= 4:
                curr.append((y,x,-dx,-dy,1,c))

    tot = target_min
    # print_grid(min_costs)
    print(tot)
    print(tot2)

# 1246