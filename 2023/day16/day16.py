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

    def print_grid(grid):
        for x in grid:
            for y in x:
                print(y, end='')
            print()
        print()
    
    m = len(grid)
    n = len(grid[0])
    for i in range(m):
        for j in range(n):
            pass
    def count_energized(x, y, dx, dy, cache={}):
        print(len(cache))
        if (x,y,dx,dy) in cache:
            return cache[(x,y,dx,dy)]

        energized = [[False for x in y] for y in grid]
        tot = 0
        curr = [(y,x,dy,dx)]
        old = []
        ends = set()
        while curr:
            y,x, dy, dx = curr.pop()
            if (y,x,dy,dx) in old:
                continue
            else:
                old.append((y,x,dy,dx))
            x += dx
            y += dy
            if x < 0 or x >= n or y < 0 or y >= m:
                ends.add((x,y,-dx,-dy))
                continue
            energized[y][x] = True
            if grid[y][x] == '-':
                if dy != 0:
                    curr.append((y,x,0,1))
                    curr.append((y,x,0,-1))
                else:
                    curr.append((y,x,dy,dx))
            if grid[y][x] == '|':
                if dx != 0:
                    curr.append((y,x,1,0))
                    curr.append((y,x,-1,0))
                else:
                    curr.append((y,x,dy,dx))
            if grid[y][x] == '\\':
                curr.append((y,x,dx,dy))
            if grid[y][x] == '/':
                curr.append((y,x,-dx,-dy))
            if grid[y][x] == '.':
                curr.append((y,x,dy,dx))
            
        for x in energized:
            for y in x:
                if y:
                    tot += 1
        for x in ends:
            cache[x] = tot
        return tot
    # energized2 = [['#' if y else '.' for y in x] for x in energized]
    # print_grid(energized2)

    tot = count_energized(-1,0,1,0)
    print(tot)
    counts = []
    for y in range(m):
        counts.append(count_energized(-1, y, 1, 0))
        counts.append(count_energized(n, y, -1, 0))
    for x in range(n):
        counts.append(count_energized(x, -1, 0, 1))
        counts.append(count_energized(x, m, 0, -1))
    tot2 = max(counts)
    print(tot2)