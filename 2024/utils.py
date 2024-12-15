def turn(dir, left=False): ## defaults to right turn
    if left:
        return (-dir[1], dir[0])
    return (dir[1], -dir[0])

def left(dir):
    return turn(dir, left=True)

def right(dir):
    return turn(dir)

def in_grid(grid, pos):
    return pos[0] >= 0 and pos[0] < len(grid) and pos[1] >= 0 and pos[1] < len(grid[pos[0]])

def get_neighbors(grid, pos, allow_empty=False):
    nbrs = []
    i, j = pos
    for nbr in [(i-1,j),(i+1,j),(i,j-1),(i,j+1)]:
        if allow_empty or in_grid(grid, nbr):
            nbrs.append(nbr)
    return nbrs

def gridrange(grid):
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            yield i,j

def cross(vec1, vec2):
    return [vec1[(i+1) % len(vec1)] * vec2[(i+2) % len(vec1)] - vec1[(i+2)%len(vec1)] * vec2[(i+1)%len(vec1)] for i in range(len(vec1))]

def dot(vec1, vec2):
    return sum([vec1[i] * vec2[i] for i in range(len(vec1))])

def sub(vec1, vec2):
    return [vec1[i]-vec2[i] for i in range(len(vec1))]

def add(vec1, vec2):
    return [vec1[i] + vec2[i] for i in range(len(vec1))]

def mul(vec, scalar):
    return [vec[i] * scalar for i in range(len(vec))]

def div(vec, scalar):
    return [vec[i] / scalar for i in range(len(vec))]

def rmap(mapping: dict):
    return {y: x for x, y in mapping.items()}

def print_grid(grid):
    for line in grid:
        line_str = ""
        for token in line:
            line_str += str(token)
        print(line_str)

def get_dir_map():
    return {"<": (-1, 0), ">":(1,0), "^": (0,1), "v": (0,-1)}

def gat(grid, pos): ## short for grid-at, grid is in y, x order
    return grid[pos[1]][pos[0]]

def step(pos, dir):
    dir_map = get_dir_map()
    if dir in dir_map:
        dir = dir_map[dir]
    return (pos[0] + dir[0], pos[1]+dir[1])