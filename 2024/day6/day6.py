import os
import re
import tqdm

basepath = os.path.dirname(os.path.abspath(__file__))

def step(pos, dir):
    return (pos[0] + dir[0], pos[1]+dir[1])

def turn(dir):
    return (dir[1], -dir[0])

def in_grid(grid, pos):
    return pos[0] >= 0 and pos[0] < len(grid) and pos[1] >= 0 and pos[1] < len(grid[pos[0]])

for filename in ['test_input.txt', 'input.txt']:
    print(filename)
    tot = 0
    tot2 = 0

    lines = []
    grid = []
    with open(os.path.join(basepath, filename), 'r') as fin:
        lines = [line.strip() for line in fin]
        grid = [[x for x in line] for line in lines]
    start = None
    start_dir = None
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == "^":
                start = (i,j)
                start_dir = (-1, 0)
    
    tot = 1
    pos = start
    dir = start_dir
    path = []
    while True:
        next_pos = step(pos, dir)
        if not in_grid(grid, next_pos):
            break
        if grid[next_pos[0]][next_pos[1]] == "#":
            dir = turn(dir)
        else:
            if grid[pos[0]][pos[1]] != "X":
                grid[pos[0]][pos[1]] = "X"
                tot += 1
            path += [(pos, dir)]
            pos = next_pos

                

    # for line in grid:
    #     print("".join(line))
    
    print(len(path))
    tried = set()
    for i in tqdm.trange(len(path)):
        grid = [[x for x in line] for line in lines]
        pos, dir = path[i]
        block_loc = step(pos, dir)
        if not in_grid(grid, block_loc):
            continue
        visited = path[:i+1]
        if block_loc in tried:
            continue
        tried.add(block_loc)
        grid[block_loc[0]][block_loc[1]] = "#"
        
        next_pos = None
        # pos = start
        # dir = start_dir
        while True:
            next_pos = step(pos, dir)
            if not in_grid(grid, next_pos):
                break
            if grid[next_pos[0]][next_pos[1]] == "#":
                dir = turn(dir)
            else:
                if grid[pos[0]][pos[1]] != "X":
                    grid[pos[0]][pos[1]] = "X"
                if (pos, dir) in visited:
                    break
                else:
                    visited.append((pos, dir))
                    # print(visited)
                pos = next_pos
        
        # for line in grid:
        #     print("".join(line))
        # input()
        if not in_grid(grid, next_pos):
            continue
        
        grid[block_loc[0]][block_loc[1]] = "O"
        # for line in grid:
        #     print("".join(line))
        # input()
        tot2 += 1
    
    print(tot)
    print(tot2)
    # break

# Took a long time to run for part 2 (~8 minutes). Afterwards I added a small speedup by skipping part of the known path, brought the runtime down to 2 minutes
# Maybe figuring out a backtracking route from each turn could've run faster, but also may have taken more than 2 minutes to code
