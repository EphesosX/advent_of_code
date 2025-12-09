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
    with open(os.path.join(basepath, filename), 'r') as fin:
        lines = [x.strip() for x in fin]
        grid = [[x for x in line] for line in lines]

    positions = [tuple(int(x) for x in line.split(",")) for line in lines]

    # print(positions)
    areas = []
    areas2 = []
    # green = []
    # for i in range(len(positions)):
    #     ip1 = (i+1) % len(positions)
    #     pos_a = positions[i]
    #     pos_b = positions[ip1]
    #     diff = sub(pos_a, pos_b)
    #     k = 0 if diff[0] != 0 else 1
    #     s = 1 if diff[k] > 0 else -1
    #     s2 = [0, 0]
    #     s2[k] = s
    #     for j in range(1, diff[k] * s - 1):
    #         green.append(add(pos_a, mul(s2, j)))

    # find turning direction
    n_right = 0
    dir = [0,0]
    diff = sub(positions[0], positions[-1])
    k = 0 if diff[0] != 0 else 1
    s = 1 if diff[k] > 0 else -1
    dir[k] = s

    for i in range(len(positions)):
        ip1 = (i+1) % len(positions)
        pos_a = positions[i]
        pos_b = positions[ip1]
        diff = sub(pos_b, pos_a)
        k = 0 if diff[0] != 0 else 1
        s = 1 if diff[k] > 0 else -1
        s2 = [0, 0]
        s2[k] = s
        if s2[k] * dir[1-k] * (1 if k == 1 else -1) == 1:
            n_right += 1
        else:
            n_right -= 1
        dir = s2
        # print(s2, n_right)

    print("right" if n_right > 0 else "left")

    def intersect(rect, line):
        pos, pos2 = rect
        pos_a, pos_b = line
        diff = sub(pos_b, pos_a)
        k = 0 if diff[0] != 0 else 1
        s = 1 if diff[k] > 0 else -1
        m = pos_a[1-k]
        if (m - pos[1-k]) * (m - pos2[1-k]) >= 0:
            return False
        if (pos[k] - pos_a[k]) * (pos[k] - pos_b[k]) > 0:
            if (pos2[k] - pos_a[k]) * (pos2[k] - pos_b[k]) > 0:
                if (pos[k] - pos_a[k]) * (pos[k] - pos_b[k]) > 0:
                    # line doesn't intersect
                    return False
        return True




    for i in range(len(positions)):
        pos = positions[i]
        for j in range(i+1, len(positions)):
            pos2 = positions[j]
            diff = sub(pos, pos2)

            area = (abs(diff[0])+1) * (abs(diff[1])+1)
            areas.append((area, i, j))

            valid = True

            
            # Too slow
            # for k in range(len(positions)):
            #     # check entire rectangle lies to the right/left of a line (if intersection)
            #     kp1 = (k+1) % len(positions)
            #     pos_a = positions[k]
            #     pos_b = positions[kp1]

                # if intersect((pos, pos2), (pos_a, pos_b)):
                #     valid = False
            #     diff = sub(pos_b, pos_a)
            #     k = 0 if diff[0] != 0 else 1
            #     s = 1 if diff[k] > 0 else -1
            #     m = pos_a[1-k]

            # if valid:
            #     areas2.append((area, i, j))
                # print(area, i, j)


    areas = sorted(areas, reverse=True)
    # print(areas)
    tot = areas[0][0]

    # new tactic, try remapping all the positions, then brute force
    
    xvals = sorted(set([x[0] for x in positions]))
    yvals = sorted(set([x[1] for x in positions]))
    xmap = {x: i for i, x in enumerate(xvals)}
    ymap = {y: i for i, y in enumerate(yvals)}

    grid = [list(["." for x in range(len(xvals))]) for y in range(len(yvals))]
    
    # print_grid(grid)

    for i in range(len(positions)):
        pos = positions[i]
        pos_mapped = [xmap[pos[0]], ymap[pos[1]]]
        ip1 = (i+1) % len(positions)
        pos2 = positions[ip1]
        pos2_mapped = [xmap[pos2[0]], ymap[pos2[1]]]
        diff = sub(pos2_mapped, pos_mapped)
        k = 0 if diff[0] != 0 else 1
        s = 1 if diff[k] > 0 else -1
        m = pos_mapped[1-k]
        grid[pos_mapped[1]][pos_mapped[0]] = "#"
        for j in range(1, diff[k] * s):
            s2 = [0,0]
            s2[k] = s * j

            new_pos = add(pos_mapped, s2)
            grid[new_pos[1]][new_pos[0]] = "X"
    # print_grid(grid)

    curr = set()
    for x in range(0, len(xmap)):
        curr.add((x,0))
        curr.add((x,len(ymap)-1))
        
    for y in range(0, len(ymap)):
        curr.add((0,y))
        curr.add((len(xmap)-1, y))
    
    while len(curr) > 0:
        new_curr = set()
        for pos in curr:
            if gat(grid, pos) == ".":
                gset(grid, pos, " ")
                for nbr in get_neighbors(grid, pos):
                    if gat(grid, nbr) == ".":
                        new_curr.add(nbr)
        curr = new_curr
    # print_grid(grid)



    for i in range(len(positions)):
        pos = positions[i]
        for j in range(i+1, len(positions)):
            pos2 = positions[j]

            pos_mapped = [xmap[pos[0]], ymap[pos[1]]]
            pos2_mapped = [xmap[pos2[0]], ymap[pos2[1]]]

            xmin = min(pos_mapped[0], pos2_mapped[0])
            xmax = max(pos_mapped[0], pos2_mapped[0])
            ymin = min(pos_mapped[1], pos2_mapped[1])
            ymax = max(pos_mapped[1], pos2_mapped[1])

            valid = True
            for x in range(xmin, xmax+1):
                for y in range(ymin, ymax+1):
                    if gat(grid, (x, y)) == " ":
                        valid = False
                        break
                if not valid:
                    break
            if valid:
                diff = sub(pos, pos2)

                area = (abs(diff[0])+1) * (abs(diff[1])+1)
                areas2.append((area, i, j))




    areas2 = sorted(areas2, reverse=True)
    tot2 = areas2[0][0]

    print(tot)
    print(tot2)
    # break

# 1h28m
# started out with a harder approach that would scale better, but couldn't get it to work
# issue was that you could have a weird concave that snakes around behind any given single line, so any checks would have to be global instead of being able to do them one line at a time
# also that there were too many lines to do the check?
# after checking the input size it looked like a brute force in the reduced space would work okay
# it's effectively O(N^4) since that's the maximum size of the reduced space times the number of rectangles
# definitely could have finished in under 20 mins if I had started with that instead of trying to figure out turning angles
