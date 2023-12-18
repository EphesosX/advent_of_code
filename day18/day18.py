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

for filename in ['test_input.txt', 'input.txt']:
    print(filename)
    data = []

    with open(os.path.join(basepath, filename), 'r') as fin:
        for line in fin:
            data.append(line.strip())

    tot = 0
    tot2 = 0

    plan = []
    for line in data:
        dir = line.split()[0]
        dist = int(line.split()[1])
        color = line.split()[2]
        plan.append((dir, dist, color))

    dir_map = {'U': (-1,0), 'D': (1,0), 'L':(0,-1), 'R': (0,1)}
    curr = [0,0]
    points = [(0,0)]
    for dir, dist, color in plan:
        curr[0] += dist * dir_map[dir][0]
        curr[1] += dist * dir_map[dir][1]
        points.append(tuple(curr))

    min_x = min([x[1] for x in points])
    max_x = max([x[1] for x in points])
    min_y = min([x[0] for x in points])
    max_y = max([x[0] for x in points])

    grid = [['.' for i in range(min_x, max_x+1)] for j in range(min_y, max_y+1)]
    colors = [[None for i in range(min_x, max_x+1)] for j in range(min_y, max_y+1)]
    curr = [0,0]
    for dir, dist, color in plan:
        for i in range(dist):
            curr[0] += dir_map[dir][0]
            curr[1] += dir_map[dir][1]
            grid[curr[0]-min_y][curr[1]-min_x] = '#'
            colors[curr[0]-min_y][curr[1]-min_x] = color
    

    in_loop2 = [[x == '.' for x in y] for y in grid]
    curr3 = []
    m = len(grid)
    n = len(grid[0])
    for i in [0, m-1]:
        for j in range(n):
            if in_loop2[i][j]:
                curr3.append((i,j))
                in_loop2[i][j] = False
    for i in range(m):
        for j in [0, n-1]:
            if in_loop2[i][j]:
                curr3.append((i,j))
                in_loop2[i][j] = False
    while curr3:
        curr4 = []
        for i, j in curr3:
            for x, y in get_neighbors(i, j, m, n):
                if not in_loop2[x][y]:
                    continue
                in_loop2[x][y] = False
                curr4.append((x,y))
        curr3 = curr4
    
    for i in range(m):
        for j in range(n):
            if in_loop2[i][j]:
                grid[i][j] = '#'

    # print_grid(grid)

    tot += sum([sum([1 if x == '#' else 0 for x in y]) for y in grid])


    #############

    plan = []
    for line in data:
        # dir = line.split()[0]
        # dist = int(line.split()[1])
        color = line.split()[2][2:-1]
        dir = ['R','D','L','U'][int(color[-1])]
        dist = int(color[:-1], 16)
        plan.append([dir, dist])

    curr = [0,0]
    points = [(0,0)]
    for dir, dist in plan:
        curr[0] += dist * dir_map[dir][0]
        curr[1] += dist * dir_map[dir][1]
        points.append(tuple(curr))

    min_x = min([x[1] for x in points])
    max_x = max([x[1] for x in points])
    min_y = min([x[0] for x in points])
    max_y = max([x[0] for x in points])

    # print(plan)

    def get_grid(plan):
        curr = [0,0]
        points = [(0,0)]
        for dir, dist in plan:
            curr[0] += dist * dir_map[dir][0]
            curr[1] += dist * dir_map[dir][1]
            points.append(tuple(curr))

        min_x = min([x[1] for x in points])
        max_x = max([x[1] for x in points])
        min_y = min([x[0] for x in points])
        max_y = max([x[0] for x in points])
        grid = [['.' for i in range(min_x, max_x+1)] for j in range(min_y, max_y+1)]
        curr = [0,0]
        for dir, dist in plan:
            for i in range(dist):
                curr[0] += dir_map[dir][0]
                curr[1] += dir_map[dir][1]
                grid[curr[0]-min_y][curr[1]-min_x] = '#'
        in_loop2 = [[x == '.' for x in y] for y in grid]
        curr3 = []
        m = len(grid)
        n = len(grid[0])
        for i in [0, m-1]:
            for j in range(n):
                if in_loop2[i][j]:
                    curr3.append((i,j))
                    in_loop2[i][j] = False
        for i in range(m):
            for j in [0, n-1]:
                if in_loop2[i][j]:
                    curr3.append((i,j))
                    in_loop2[i][j] = False
        while curr3:
            curr4 = []
            for i, j in curr3:
                for x, y in get_neighbors(i, j, m, n):
                    if not in_loop2[x][y]:
                        continue
                    in_loop2[x][y] = False
                    curr4.append((x,y))
            curr3 = curr4
        
        for i in range(m):
            for j in range(n):
                if in_loop2[i][j]:
                    grid[i][j] = '#'

        return grid
    # test input clockwise, input ccw

    opp = {'R':'L', 'L':'R', 'U':'D', 'D': 'U'}
    clock_map = {'U':'R', 'R':'D', 'D':'L', 'L':'U'}
    if filename[0] == 't' or True:
        clock_map = {y:x for x,y in clock_map.items()}

    # simplify to a box with missing parts
    while len(plan) > 4:
        curr_dir = plan[0][0]
        next_dir = plan[1][0]
        nn_dir = plan[2][0]
        if plan[1][1] == 0:
            if nn_dir == curr_dir:
                plan[0][1] += plan[2][1]
                del plan[2]
                del plan[1]
            elif nn_dir == opp[curr_dir]:
                if plan[0][1] > plan[2][1]:
                    plan[0][1] -= plan[2][1]
                    del plan[2]
                    del plan[1]
                else:
                    plan[2][1] -= plan[0][1]
                    del plan[1]
                    del plan[0]
        else:
            if nn_dir == curr_dir:
                nnn_dir = plan[3][0]
                if clock_map[curr_dir] == next_dir:
                    if nnn_dir == next_dir:
                        # print('case 1')
                        # staircase with chunk missing
                        tot2 += plan[1][1] * plan[2][1]
                        plan[0][1] += plan[2][1]
                        plan[1][1] += plan[3][1]
                        del plan[3]
                        del plan[2]
                    elif nnn_dir == opp[next_dir]:
                        # print('case 2')
                        # # square wave
                        # if plan[1][1] < plan[3][1]:
                        #     plan[0][1] += plan[2][1]
                        #     print('case 2-1')
                        #     tot2 += plan[1][1] * (plan[2][1]+1)
                        #     plan[3][1] -= plan[1][1]
                        #     del plan[2]
                        #     del plan[1]
                        # else:
                        # # if plan[1][1] >= plan[3][1]:
                        #     plan[0][1] += plan[2][1]
                        #     print('case 2-2')
                        #     tot2 += plan[1][1] * plan[2][1] + plan[3][1]
                        #     plan[1][1] -= plan[3][1]
                        #     del plan[3]
                        #     del plan[2]
                        # else:
                        step = plan[0]
                        del plan[0]
                        plan.append(step)

                elif opp[clock_map[curr_dir]] == next_dir:                    
                    if nnn_dir == next_dir:
                        # print('case 3')
                        # staircase with chunk missing
                        tot2 -= plan[1][1] * plan[2][1]
                        plan[0][1] += plan[2][1]
                        plan[1][1] += plan[3][1]
                        del plan[3]
                        del plan[2]
                    elif nnn_dir == opp[next_dir]:
                        # print('case 4')
                        # square wave
                        # if plan[1][1] < plan[3][1]:
                        #     print('case 4-1')
                        # plan[0][1] += plan[2][1]
                        #     tot2 -= plan[1][1] * (plan[2][1]-1)
                        #     plan[3][1] -= plan[1][1]
                        #     del plan[2]
                        #     del plan[1]
                        # if plan[1][1] > plan[3][1]:
                        #     plan[0][1] += plan[2][1]
                        #     tot2 -= plan[1][1] * plan[2][1] - plan[3][1]
                        #     plan[1][1] -= plan[3][1]
                        #     del plan[3]
                        #     del plan[2]
                        # else:
                        step = plan[0]
                        del plan[0]
                        plan.append(step)
            elif nn_dir == opp[curr_dir]:
                if plan[0][1] > plan[2][1]:
                    nnn_dir = plan[3][0]
                    if nnn_dir == next_dir:
                        if clock_map[curr_dir] == next_dir:
                            tot2 -= (plan[1][1]-1) * plan[2][1]
                            plan[0][1] -= plan[2][1]
                            plan[3][1] += plan[1][1]
                            del plan[2]
                            del plan[1]
                        else:
                            tot2 += (plan[1][1]+1) * plan[2][1]
                            plan[0][1] -= plan[2][1]
                            plan[3][1] += plan[1][1]
                            del plan[2]
                            del plan[1]
                    else:
                        step = plan[0]
                        del plan[0]
                        plan.append(step)
                else:
                    step = plan[0]
                    del plan[0]
                    plan.append(step)
        # print(plan)
        # grid = get_grid(plan)
        # print_grid(grid)
        # with open('test.out', 'w') as fout:
        #     fout.write(stringify_grid(grid))
        # print(tot2 + sum([sum([1 if x == '#' else 0 for x in y]) for y in grid]))
        # input()

    tot2 += (plan[0][1]+1) * (plan[1][1]+1)


    print(tot)
    print(tot2)
    # break
