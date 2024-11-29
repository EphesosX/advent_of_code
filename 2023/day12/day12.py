import os
basepath = os.path.dirname(os.path.abspath(__file__))

def get_neighbors2(i, j, m, n):
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

    springs = []
    groups = []
    
    for line in data:
        springs.append(line.split()[0])
        groups.append([int(x) for x in line.split()[1].split(",")])
    
    for spring, group in zip(springs, groups):
        # if group[0] != 3:
        #     continue
        cache = {}
        spring = '?'.join([spring] * 5)
        group = group * 5

        # print(spring, group)
        def f(group_idx, spring_num, spring_count, spring_i):
            params = (group_idx, spring_num, spring_count, spring_i)
            if params in cache:
                return cache[params]
            if spring_i == '.':
                if spring_count != 0:
                    if spring_count != group[group_idx]:
                        return 0
                    group_idx += 1
                    spring_count = 0
                spring_num += 1
                if spring_num == len(spring):
                    if group_idx == len(group):
                        return 1
                    else:
                        return 0
                spring_i = spring[spring_num]
                params = (group_idx, spring_num, spring_count, spring_i)
                if params in cache:
                    return cache[params]
                else:
                    cache[params] = f(group_idx, spring_num, spring_count, spring_i)
                    return cache[params]
            elif spring_i == "#":
                if group_idx >= len(group):
                    return 0
                spring_count += 1
                spring_num += 1
                if spring_num == len(spring):
                    if spring_count == group[group_idx] and group_idx == len(group) - 1:
                        return 1
                    else:
                        return 0
                spring_i = spring[spring_num]
                if spring_count > group[group_idx]:
                    return 0
                params = (group_idx, spring_num, spring_count, spring_i)
                if params in cache:
                    return cache[params]
                else:
                    cache[params] = f(group_idx, spring_num, spring_count, spring_i)
                    return cache[params]
            elif spring_i == "?":
                return f(group_idx, spring_num, spring_count, '.') + f(group_idx, spring_num, spring_count, '#')
        
        tot += f(0,0,0, spring[0])
        # print('t', f(0,0,0, spring[0]))
    print(tot)
    print(tot2)