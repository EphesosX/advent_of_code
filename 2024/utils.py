def step(pos, dir):
    return (pos[0] + dir[0], pos[1]+dir[1])

def turn(dir):
    return (dir[1], -dir[0])

def in_grid(grid, pos):
    return pos[0] >= 0 and pos[0] < len(grid) and pos[1] >= 0 and pos[1] < len(grid[pos[0]])

def get_neighbors(grid, pos):
    nbrs = []
    i, j = pos
    for nbr in [(i-1,j),(i+1,j),(i,j-1),(i,j+1)]:
        if in_grid(grid, nbr):
            nbrs.append(nbr)
    return nbrs

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