import math
from typing import List, Any, Tuple, Dict

def turn(dir, left=False) -> Tuple[int]: ## defaults to right turn
    if left:
        return (-dir[1], dir[0])
    return (dir[1], -dir[0])

def left(dir) -> Tuple[int]:
    return turn(dir, left=True)

def right(dir) -> Tuple[int]:
    return turn(dir)

def in_grid(grid: List[List[Any]], pos) -> bool:
    return pos[1] >= 0 and pos[1] < len(grid) and pos[0] >= 0 and pos[0] < len(grid[pos[1]])

def get_neighbors(grid: List[List[Any]], pos, allow_empty=False):
    nbrs = []
    i, j = pos
    for nbr in [(i-1,j),(i+1,j),(i,j-1),(i,j+1)]:
        if allow_empty or in_grid(grid, nbr):
            nbrs.append(nbr)
    return nbrs

def gridrange(grid: List[List[Any]]):
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            yield i,j

def cross(vec1, vec2) -> Tuple[Any]:
    return tuple([vec1[(i+1) % len(vec1)] * vec2[(i+2) % len(vec1)] - vec1[(i+2)%len(vec1)] * vec2[(i+1)%len(vec1)] for i in range(len(vec1))])

def dot(vec1, vec2) -> Any:
    return sum([vec1[i] * vec2[i] for i in range(len(vec1))])

def sub(vec1, vec2) -> Tuple[Any]:
    return tuple([vec1[i]-vec2[i] for i in range(len(vec1))])

def add(vec1, vec2) -> Tuple[Any]:
    return tuple([vec1[i] + vec2[i] for i in range(len(vec1))])

def mul(vec, scalar) -> Tuple[Any]:
    return tuple([vec[i] * scalar for i in range(len(vec))])

def div(vec, scalar) -> Tuple[Any]:
    return tuple([vec[i] / scalar for i in range(len(vec))])

def rmap(mapping: dict) -> dict:
    return {y: x for x, y in mapping.items()}

def print_grid(grid: List[List[Any]]):
    for line in grid:
        line_str = ""
        for token in line:
            line_str += str(token)
        print(line_str)

def get_dir_map():
    return {"<": (-1, 0), ">":(1,0), "^": (0,1), "v": (0,-1)}

def gat(grid: List[List[Any]], pos): ## short for grid-at, grid is in y, x order
    return grid[pos[1]][pos[0]]

def step(pos, dir) -> Tuple[Any]:
    dir_map = get_dir_map()
    if isinstance(dir, str) and dir in dir_map:
        dir = dir_map[dir]
    return (pos[0] + dir[0], pos[1]+dir[1])

def find_startend(grid: List[List[Any]]) -> Tuple[Tuple[int], Tuple[int]]:
    start = end = None
    for i,j in gridrange(grid):
        if grid[i][j] == "S":
            start = (j,i)
        elif grid[i][j] == "E":
            end = (j, i)
    return start, end

def get_distmap(grid: List[List[Any]], start) -> Dict[Tuple[int], int]:
    start_dist = {start: 0}
    curr = [start]
    while curr:
        next_node = curr.pop(0)
        for nbr in get_neighbors(grid, next_node):
            if gat(grid, nbr) == "#":
                continue
            if nbr in start_dist:
                if start_dist[nbr] > start_dist[next_node] + 1:
                    start_dist[nbr] = min(start_dist[nbr], start_dist[next_node] + 1)
                    curr.append(nbr)
            else:
                start_dist[nbr] = start_dist[next_node] + 1
                curr.append(nbr)
    return start_dist

def euclidean(pos, pos2):
    return abs(pos2[0] - pos[0]) + abs(pos2[1]-pos[1])

def dist2(pos, pos2):
    return (pos2[0] - pos[0]) ** 2 + (pos2[1]-pos[1]) ** 2

def dist(pos, pos2) -> float:
    return math.sqrt(dist2(pos, pos2))

def overlap(r1, r2): # checks if two ranges overlap
    if r1[0] <= r2[0] and r1[1] >= r2[0]:
        return True
    if r1[0] > r2[0] and r1[0] <= r2[1]:
        return True
    return False

def merge_ranges(r1, r2):
    return (min(r1[0], r2[0]), max(r1[1], r2[1]))