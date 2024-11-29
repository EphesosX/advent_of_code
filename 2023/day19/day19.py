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

    workflows = {}
    ratings = []
    workflow_end = False
    for line in data:
        if not line:
            workflow_end = True
            continue
        if not workflow_end:
            name = line.split("{")[0]
            workflow = line.split("{")[1][:-1].split(",")
            workflows[name] = workflow
        else:
            rating = {}
            for x in line[1:-1].split(","):
                rating[x.split("=")[0]] = int(x.split("=")[1])
            ratings.append(rating)

    for rating in ratings:
        curr = "in"
        while curr not in ["A", "R"]:
            workflow = workflows[curr]
            for rule in workflow:
                if ":" in rule:
                    cond = rule.split(":")[0]
                    dest = rule.split(":")[1]
                    if ">" in cond:
                        key = cond.split(">")[0]
                        val = int(cond.split(">")[1])
                        if rating[key] > val:
                            curr = dest
                            break
                    elif "<" in cond:
                        key = cond.split("<")[0]
                        val = int(cond.split("<")[1])
                        if rating[key] < val:
                            curr = dest
                            break
                    else:
                        raise Exception()
                else:
                    curr = rule
                    break
        if curr == "A":
            tot += sum(rating.values())

    print(tot)

    
    paths = [["in", {'x': [0,4001], 'm':[0,4001], 'a':[0,4001], 's':[0,4001]}]]
    accepted = []

    while paths:
        path = paths.pop()
        if path[0] == "A":
            accepted.append(path)
            continue
        elif path[0] == "R":
            continue
        workflow = workflows[path[0]]
        bounds = path[1] # noninclusive bounds
        for rule in workflow:
            if ":" in rule:
                cond = rule.split(":")[0]
                dest = rule.split(":")[1]
                if ">" in cond:
                    key = cond.split(">")[0]
                    val = int(cond.split(">")[1])
                    if key in bounds:
                        if bounds[key][0] is not None and bounds[key][0] >= val: # always passes
                            paths.append((dest, {x:y for x, y in bounds.items()}))
                            break
                        else:
                            new_bounds = {x: [z for z in y] for x,y in bounds.items()}
                            new_bounds[key][0] = val
                            if new_bounds[key][1] is None or new_bounds[key][1] > val:
                                paths.append([dest, new_bounds])
                            if bounds[key][1] is not None:
                                bounds[key][1] = min(bounds[key][1], val+1)
                            else:
                                bounds[key][1] = val + 1
                    else:
                        new_bounds = {x: [z for z in y] for x,y in bounds.items()}
                        new_bounds[key] = [val, None]
                        paths.append((dest, new_bounds))
                        bounds[key] = [None, val + 1]
                    
                elif "<" in cond:
                    key = cond.split("<")[0]
                    val = int(cond.split("<")[1])
                    if key in bounds:
                        if bounds[key][1] is not None and bounds[key][1] <= val: # always passes
                            paths.append((dest, {x:y for x, y in bounds.items()}))
                            break
                        else:
                            new_bounds = {x: [z for z in y] for x,y in bounds.items()}
                            new_bounds[key][1] = val
                            if new_bounds[key][0] is None or new_bounds[key][0] < val:
                                paths.append((dest, new_bounds))
                            if bounds[key][0] is not None:
                                bounds[key][0] = max(bounds[key][0], val-1)
                            else:
                                bounds[key][0] = val - 1
                    else:
                        new_bounds = {x: [z for z in y] for x,y in bounds.items()}
                        new_bounds[key] = [None, val]
                        paths.append([dest, new_bounds])
                        bounds[key] = [val - 1, None]
                else:
                    raise Exception()
            else:
                paths.append((rule, {x:y for x, y in bounds.items()}))
                break

    print(accepted)
    for x, bounds in accepted:
        num_ways = 1
        for key, bound in bounds.items():
            num_ways *= bound[1] - bound[0] - 1
        tot2 += num_ways
    print(tot2)
