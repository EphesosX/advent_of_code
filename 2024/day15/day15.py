import os
import re
import tqdm
import sys
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
from utils import *

basepath = os.path.dirname(os.path.abspath(__file__))

for filename in ['test_input.txt', 'input.txt']:
    print(filename)
    tot = 0
    tot2 = 0

    lines = []
    grid = []
    moves = []
    with open(os.path.join(basepath, filename), 'r') as fin:
        lines = [x.strip() for x in fin]
        midpoint = [i for i in range(len(lines)) if not lines[i].strip()][0]
        grid = [[x for x in line] for line in lines[:midpoint]]
        moves = [line.strip() for line in lines[midpoint+1:]]

    # print_grid(grid)
    # print_grid(moves)
    grid = grid[::-1] # invert y
    moves = "".join(moves)
    dir_map = {"<": (-1, 0), ">":(1,0), "^": (0,1), "v": (0,-1)}
    # remember x = j y = i

    robot = None
    for i,j in gridrange(grid):
        if grid[i][j] == "@":
            robot = (j, i)
    
    for move in moves:
        x, y = step(robot, dir_map[move])
        if grid[y][x] == "#":
            continue
        elif grid[y][x] == ".":
            grid[y][x] = "@"
            grid[robot[1]][robot[0]] = "."
            robot = (x, y)
        elif grid[y][x] == "O":
            curr = (x,y)
            while grid[curr[1]][curr[0]] == "O":
                curr = step(curr, dir_map[move])
            if grid[curr[1]][curr[0]] == "#":
                continue
            elif grid[curr[1]][curr[0]] == ".":
                grid[curr[1]][curr[0]] = "O"
                grid[y][x] = "@"
                grid[robot[1]][robot[0]] = "."
                robot = (x, y)
    
    # uninvert
    grid = grid[::-1]
    for i, j in gridrange(grid):
        if grid[i][j] == "O":
            tot += 100 * i + j

    
    def parse_line(line):
        l = ""
        for x in line:
            if x == "#":
                l += "##"
            elif x == ".":
                l += ".."
            elif x == "O":
                l += "[]"
            elif x == "@":
                l += "@."
        return l
    grid = [[x for x in parse_line(line)] for line in lines[:midpoint]]

    grid = grid[::-1]

    robot = None
    for i,j in gridrange(grid):
        if grid[i][j] == "@":
            robot = (j, i)
    
    for move in moves:
        x, y = step(robot, dir_map[move])
        if grid[y][x] == "#":
            continue
        elif grid[y][x] == ".":
            grid[y][x] = "@"
            grid[robot[1]][robot[0]] = "."
            robot = (x, y)
        elif grid[y][x] == "[" or grid[y][x] == "]":
            curr_moving = set([(x,y)])
            if dir_map[move][0] == 0:
                if grid[y][x] == "[":
                    curr_moving.add((x+1,y))
                else:
                    curr_moving.add((x-1,y))
            all_moving = [pos for pos in curr_moving]
            moving = True
            should_move = True
            while moving:
                # print_grid(grid)
                # print(x, y)
                # print(move, curr_moving)
                # input()
                next_moving = set()
                for loc in curr_moving:
                    nx, ny = step(loc, dir_map[move])
                    # print(nx, ny)
                    if grid[ny][nx] == "[":
                        if dir_map[move][0] == 0:
                            next_moving.add((nx, ny))
                            next_moving.add((nx+1, ny))
                        else:
                            next_moving.add((nx, ny))
                    elif grid[ny][nx] == "]":
                        if dir_map[move][0] == 0:
                            next_moving.add((nx, ny))
                            next_moving.add((nx-1, ny))
                        else:
                            next_moving.add((nx, ny))
                    elif grid[ny][nx] == ".":
                        pass
                    elif grid[ny][nx] == "#":
                        should_move = False
                        break
                if len(next_moving) == 0 or not should_move:
                    moving = False
                else:
                    for pos in next_moving:
                        all_moving.append(pos)
                    curr_moving = next_moving
                
            if should_move:
                # print(all_moving)
                for loc in all_moving[::-1]:
                    next_loc = step(loc, dir_map[move])
                    grid[next_loc[1]][next_loc[0]] = grid[loc[1]][loc[0]]
                    grid[loc[1]][loc[0]] = "."
                if dir_map[move][0] != 0:
                    grid[y][x] = "@"
                else:
                    if grid[y][x] == "[":
                        grid[y][x] = "@"
                        grid[y][x+1] = "."
                    elif grid[y][x] == "]":
                        grid[y][x] = "@"
                        grid[y][x-1] = "."
                grid[robot[1]][robot[0]] = "."
                robot = (x, y)

    # uninvert
    grid = grid[::-1]
    for i, j in gridrange(grid):
        if grid[i][j] == "[":
            tot2 += 100 * i + j
    # print_grid(grid)
    print(tot)
    print(tot2)
    # break

## Super messy doing everything in text, maybe I should've done it in coordinates (track location of each box instead)
## lots of issues like moving half a box without the other half, forgetting to remove half the box when moving the other half, etc.
## being able to just printgrid and see it exactly as the example shows it is nice though
## also made really sure to keep x and y straight after yesterday, very cumbersome though, should probably add more helpers