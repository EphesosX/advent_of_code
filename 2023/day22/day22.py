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

    bricks = []
    for line in data:
        pos, pos2 = line.split("~")
        pos = [int(x) for x in pos.strip().split(",")]
        pos2 = [int(x) for x in pos2.strip().split(",")]
        bricks.append((pos, pos2))
    
    bricks = sorted(bricks, key=lambda x: min(x[0][-1], x[1][-1]))

    def has_intersection(brick, brick2):
        min_x = min(brick[0][0], brick[1][0])
        max_x = max(brick[0][0], brick[1][0])
        min_y = min(brick[0][1], brick[1][1])
        max_y = max(brick[0][1], brick[1][1])
        min_x2 = min(brick2[0][0], brick2[1][0])
        max_x2 = max(brick2[0][0], brick2[1][0])
        min_y2 = min(brick2[0][1], brick2[1][1])
        max_y2 = max(brick2[0][1], brick2[1][1])
        if (min_x <= min_x2 and max_x >= min_x2) or (min_x > min_x2 and min_x <= max_x2):
            if (min_y <= min_y2 and max_y >= min_y2) or (min_y > min_y2 and min_y <= max_y2):
                return True
        return False

    def settle(bricks):
        supports = []
        for i, brick in enumerate(bricks):
            support = [-1]
            new_z = 1
            for j in range(i):
                brick2 = bricks[j]
                if has_intersection(brick, brick2):
                    if max(brick2[0][-1], brick2[1][-1]) >= new_z:
                        new_z = max(brick2[0][-1], brick2[1][-1]) + 1
                        support = [j]
                    elif max(brick2[0][-1], brick2[1][-1]) + 1 == new_z:
                        support.append(j)
                        
            min_z = min(brick[0][-1], brick[1][-1])
            delta = min_z - new_z
            brick[0][-1] -= delta
            brick[1][-1] -= delta
            supports.append(support)
        return supports
    supports = settle(bricks)
    can_disintegrate = [True for _ in bricks]
    for support in supports:
        if len(support) == 1:
            if support[0] != -1:
                can_disintegrate[support[0]] = False
    # print(can_disintegrate)
    # print(supports)
    tot = sum([1 if x else 0 for x in can_disintegrate])
    print(tot)

    n_fall = [0 for _ in bricks]
    for i in range(len(bricks)):
        falling = set()
        new_falling = {i}
        while new_falling:
            new_fall = new_falling.pop()
            falling.add(new_fall)
            for j in range(len(supports)):
                if j not in falling:
                    will_fall = True
                    for x in supports[j]:
                        if x not in falling:
                            will_fall = False
                    if will_fall:
                        new_falling.add(j)
        n_fall[i] = len(falling) - 1

    print(n_fall)
    tot2 = sum(n_fall)

    print(tot2)
    # break