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

    tot = 0
    tot2 = 0
    grid = []
    for line in data:
        grid.append([x for x in line])
    m = len(grid)
    n = len(grid[0])
    print(m,n)
    for i in range(m):
        for j in range(n):
            if grid[i][j] == 'S':
                start = (i, j)
                grid[i][j] = '.'

    print(start)
    n_steps = 1000
    target = 26501365
    # target = 5000

    curr = {start}
    visited = set()
    visited2 = set()
    visited1 = set()
    visited_sizes = []
    for i in range(0, n_steps+1):
        next = set()
        for point in curr:
            for neighbor in [(point[0]-1, point[1]), (point[0]+1, point[1]), (point[0], point[1]-1),(point[0], point[1]+1)]:
                if neighbor not in visited and grid[neighbor[0] % m][neighbor[1] % n] != '#':
                    next.add(neighbor)
            visited.add(point)
            if i % 2 == 0:
                visited2.add(point)
            else:
                visited1.add(point)
        if i % m == target % m:
            if i % 2 == 0:
                visited_sizes.append(len(visited2))
            else:
                visited_sizes.append(len(visited1))
        curr = next
    print(f"Visited {len(visited2) if n_steps % 2 == 0 else len(visited1)} nodes in {n_steps} steps")
    # for i in range(m):
    #     line = ""
    #     for j in range(n):
    #         if (i,j) in (visited2 if n_steps % 2 == 0 else visited1):
    #             line += "O"
    #         else:
    #             line += grid[i][j]
    #     print(line)

    # continue

    # print(visited_sizes)
    diffs = [visited_sizes[i] - visited_sizes[i-1] for i in range(1, len(visited_sizes))]
    # print(diffs)
    diffs2 = [diffs[i]-diffs[i-1] for i in range(1, len(diffs))]
    # print(diffs2)
    diffs3 = [diffs2[i]-diffs2[i-1] for i in range(1, len(diffs2))]
    # print(diffs3)
    n_iters = 26501365 / m
    print("Number of iterations: ", n_iters)
    coeff2 = diffs2[-1] / 2
    coeff1 = diffs[5] - coeff2
    coeff0 = visited_sizes[5]
    print(visited_sizes)
    print([int(coeff0 + coeff1 * i + coeff2 * (i ** 2)) for i in range(len(visited_sizes)-5)])
    print(int(target / m) - 5)
    print(len(visited_sizes) - 5)

    n_iters = int(target / m) - 5
    print(int(coeff0 + coeff1 * n_iters + coeff2 * (n_iters ** 2)))
    continue

    # 470149643712804


    # floodfill 64, even cells reachable
    curr = [start]
    grid2 = [[x for x in y] for y in grid]
    grid2[start[0]][start[1]] = 'O'
    visited = []
    visited.append(start)
    for _ in range(n_steps):
        next_curr = []
        for i, j in curr:
            for i2, j2 in get_neighbors(i, j, m, n):
                if grid2[i2][j2] == '.':
                    visited.append((i2, j2))
                    next_curr.append((i2, j2))
                    grid2[i2][j2] = 'O'
        curr = next_curr
        # print(stringify_grid(grid))
        # print(curr)
        # input()
    
    # print(visited)
    for i, j in visited:
        if (i+j)%2 == (start[0] + start[1])%2:
            # print(i, j)
            tot += 1

    print(f"Total visitable points in {n_steps} steps:", tot)

    # starting at a corner, can reach the corresponding corner in m+n steps by going around the outside
    # assume no straight line paths through grid other than on edges
    
    # n_steps = 26501365
    iter_counts = []
    for iter in range(1,6):
    # for n_steps in [6, 10, 50, 100, 500, 1000, 5000]:
        tot2 = 0
        n_steps = 65 + m*iter
        # print(f"Calculating total for {n_steps} steps")

        # dist from start to corner
        dist_corner = {(0,0): 0, (0,n-1): 0, (m-1,0): 0, (m-1,n-1): 0}
        
        curr = [start]
        grid2 = [[x for x in y] for y in grid]
        grid2[start[0]][start[1]] = 'O'
        visited = []
        visited.append(start)
        k = 0
        while curr:
            k += 1
            next_curr = []
            for i, j in curr:
                for i2, j2 in get_neighbors(i, j, m, n):
                    if grid2[i2][j2] == '.':
                        visited.append((i2, j2))
                        next_curr.append((i2, j2))
                        grid2[i2][j2] = 'O'
                        if (i2, j2) in dist_corner:
                            dist_corner[(i2, j2)] = k
            curr = next_curr

        # print("Distance to corners: ", dist_corner)

        # number of steps to fully fill grid from each corner
        max_fill = {(0,0): 0, (0,n-1): 0, (m-1,0): 0, (m-1,n-1): 0}
        for start_i in max_fill:
            curr = [start_i]
            grid2 = [[x for x in y] for y in grid]
            grid2[start[0]][start[1]] = 'O'
            visited = []
            visited.append(start)
            k = 0
            while curr:
                k += 1
                next_curr = []
                for i, j in curr:
                    for i2, j2 in get_neighbors(i, j, m, n):
                        if grid2[i2][j2] == '.':
                            visited.append((i2, j2))
                            next_curr.append((i2, j2))
                            grid2[i2][j2] = 'O'
                curr = next_curr
            max_fill[start_i] = k - 1
        # print("Steps to fully fill grid from each corner: ", max_fill)
        grid_size = len(visited)
        even_grid_size = len([x for x in visited if (sum(x) + sum(start)) % 2 == 0])
        odd_grid_size = len([x for x in visited if (sum(x) + sum(start)) % 2 == 1])
        # print("Number of reachable squares starting from an even coordinate: ", even_grid_size)
        # print("Number of reachable squares starting from an odd coordinate: ", odd_grid_size)

        # rem = (n_steps - m-1) % m
        # n_grid_steps = (n_steps-m-1) // m
        # print(n_grid_steps)
        # print(f"Remaining steps after {n_grid_steps} grids filled: ", rem)
        # # # 1, 5, 13, 25, 41, 61, 85 ... = 1+4*(k*k+1)/2
        # # # 1, 9, 25, ... = (2k+1) ** 2
        # # # 4, 16, 36, 64, ... = 4*(k+1) ** 2
        # # grid_filled = (n_grid_steps // 2 + 1)**2 * even_grid_size
        # # grid_filled += 4*(n_grid_steps//2 + 1)**2 * odd_grid_size
        # grid_filled = (1 + 4 * (n_grid_steps*(n_grid_steps+1)//2)) * odd_grid_size
        # print("Number of squares from completely filled grids: ", grid_filled)

        # tot2 = grid_filled
        # rem_fill = {}
        # for corner in max_fill:
        #     curr = [corner]
        #     grid2 = [[x for x in y] for y in grid]
        #     grid2[start[0]][start[1]] = 'O'
        #     visited = []
        #     visited.append(start)
        #     k = 0
        #     # Step to a corner, then go down/across n_grid_steps
        #     rem_i = n_steps - dist_corner[corner] - n_grid_steps * m - 2
        #     print('Remaining steps to take: ', corner, ' ', rem_i)
        #     while k < rem_i:
        #         k += 1
        #         next_curr = []
        #         for i, j in curr:
        #             for i2, j2 in get_neighbors(i, j, m, n):
        #                 if grid2[i2][j2] == '.':
        #                     visited.append((i2, j2))
        #                     next_curr.append((i2, j2))
        #                     grid2[i2][j2] = 'O'
        #         curr = next_curr
        #     rem_fill[corner] = len(visited)
        #     tot2 += len(visited) * (n_grid_steps + 1)
        # print(rem_fill)


        # Big grid composed of tiles
        n_full_tiles = 0
        n_partial_tiles = 0
        max_tile_steps = n_steps // m + 1
        cache = {}
        for a2 in range(-max_tile_steps, max_tile_steps):
            for b2 in range(-max_tile_steps, max_tile_steps):
                # if (abs(a2)+abs(b2)+1) * m + max(dist_corner.values()) < n_steps:
                #     n_full_tiles += 1
                #     tot2 += odd_grid_size if (a2+b2) % 2 == 1 else even_grid_size
                #     grid_full = True
                #     continue
                dist_tile_corner = {} # Shortest distance from the start to this corner
                grid_full = False
                for corner in dist_corner:
                    tile_corner = (corner[0] + a2 * m, corner[1] + b2*n)
                    dist_tile_corner[corner] = min([abs(x-tile_corner[0]) + abs(y-tile_corner[1]) + dist_corner[x,y] for x,y in dist_corner])
                    if dist_tile_corner[corner] + max_fill[corner] <= n_steps:
                        n_full_tiles += 1
                        tot2 += odd_grid_size if (n_steps - dist_tile_corner[corner]) % 2 == 1 else even_grid_size
                        grid_full = True
                        break
                if grid_full:
                    continue
                key = tuple(sorted((tile_corner, dist) for tile_corner, dist in dist_tile_corner.items()))
                # if key in cache:
                #     tot2 += cache[key]
                #     n_partial_tiles += 1
                #     continue
                # print(a2, b2, dist_tile_corner)
                visited = set()
                if a2 == 0 and b2 == 0:
                    dist_tile_corner = {start: 0}
                for tile_corner, dist in dist_tile_corner.items():
                    if dist > n_steps:
                        continue
                    grid2 = [[x for x in y] for y in grid]
                    rem_fill = {}
                    curr = [tile_corner]
                    if (n_steps - dist) % 2 == 0:
                        visited.add(tile_corner)
                    grid2[tile_corner[0]][tile_corner[1]] = 'O'
                    k = 0
                    rem_i = n_steps - dist
                    # print('Remaining steps to take: ', tile_corner, ' ', rem_i)
                    while k < rem_i:
                        k += 1
                        next_curr = []
                        for i, j in curr:
                            for i2, j2 in get_neighbors(i, j, m, n):
                                if grid2[i2][j2] == '.':
                                    if (n_steps - dist - k) % 2 == 0:
                                        visited.add((i2, j2))
                                    next_curr.append((i2, j2))
                                    grid2[i2][j2] = 'O'
                        curr = next_curr
                    rem_fill[tile_corner] = len(visited)
                tot2 += len(visited)
                if len(visited) > 0:
                    n_partial_tiles += 1
                    cache[key] = len(visited)
        # print("Number of filled tiles: ", n_full_tiles)
        # print("Number of partial tiles: ", n_partial_tiles)
        print(n_steps, tot2)
        iter_counts.append(tot2)
        # break
    # polynomial fit
    print(iter_counts)
    iter_dict2 = [iter_counts[i+1] - iter_counts[i] for i in range(len(iter_counts)-1)]
    print(iter_dict2)
    iter_dict3 = [iter_dict2[i+1] - iter_dict2[i] for i in range(len(iter_dict2)-1)]
    print(iter_dict3)
    iter_dict4 = [iter_dict3[i+1] - iter_dict3[i] for i in range(len(iter_dict3)-1)]
    print(iter_dict4)
    
    if (iter_dict4[0] == iter_dict4[1]):
        # Multiply all coeffs by 6 for rationality
        coeff_3 = iter_dict4[0]
        coeff_2 = (iter_dict3[0] - 2 * coeff_3) * 3
        coeff_1 = (iter_dict2[0]*6 - 3 * coeff_2 - 7 * coeff_3)
        coeff_0 = (iter_counts[0]*6 - coeff_1 - coeff_2 - coeff_3)
        print(coeff_3, coeff_2, coeff_1, coeff_0)
        for x in range(1,6):
            print((coeff_3 * x**3 + coeff_2 * x**2 + coeff_1 * x + coeff_0) / 6)
        x = 26501365 // m
        print(x)
        print(65 + x * m)
        print((coeff_3 * x**3 + coeff_2 * x**2 + coeff_1 * x + coeff_0) // 6, (coeff_3 * x**3 + coeff_2 * x**2 + coeff_1 * x + coeff_0) % 6)

    # 41145407968053149696 too high
    # 41145407968053140567 too high
    # 610158187347418 too low 
    # 610158187362102