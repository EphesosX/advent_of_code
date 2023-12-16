import os
basepath = os.path.dirname(os.path.abspath(__file__))

for filename in ['test_input.txt', 'input.txt']:
    print(filename)
    data = []

    with open(os.path.join(basepath, filename), 'r') as fin:
        for line in fin:
            data.append(line.strip())


    tot = 0
    tot2 = 0
    map = {}
    direction = ""    
    for i, line in enumerate(data):
        if i == 0:
            direction = line
            continue 
        elif i == 1:
            continue
        key, vals = line.strip().split("=")
        left, right = vals.strip().split(",")
        map[key.strip()] = (left.strip()[1:], right.strip()[:-1])

    # curr = 'AAA'

    # while curr != "ZZZ":
    #     tot += 1
    #     dir = direction[0]
    #     direction = direction[1:] + dir
    #     curr = map[curr][0] if dir == "L" else map[curr][1]
    # if filename[0] == 't':
    #     print(map, direction)
    print(tot)

    nodes = []
    for key in map:
        if key[-1] == 'A':
            nodes.append(key)
    
    z_cycles = {}
    # z_nodes = []
    # for key in map:
    #     if key[-1] == 'Z':
    #         z_nodes.append(key)
    # for z_node in z_nodes:
    #     for i in range(len(direction)):
    #         cycle_len = 0
    #         curr = z_node
    #         j = i
    #         while cycle_len == 0 or curr != z_node or j != i:
    #             cycle_len += 1
    #             dir = direction[j]
    #             j += 1
    #             j %= len(direction)
    #             curr = map[curr][0] if dir == "L" else map[curr][1]
    #         z_cycles[(z_node, j)] = cycle_len

    i = 0
    # while sum([1 for x in nodes if x[-1] != "Z"]) > 0:
    #     tot2 += 1
    #     dir = direction[i]
    #     i += 1
    #     i %= len(direction)
        # nodes = [(map[curr][0] if dir == "L" else map[curr][1]) for curr in nodes]
    #     for i in range(len(nodes)):
    #         if nodes[i][-1] == 'Z':
    #             z_node = nodes[i]
    #             if i in z_cycles and z_node in z_cycles[i]:
    #                 continue
    #             cycle_len = 0
    #             curr = z_node
    #             j = i
    #             while cycle_len == 0 or curr != z_node or j != i:
    #                 cycle_len += 1
    #                 dir2 = direction[j]
    #                 j += 1
    #                 j %= len(direction)
    #                 curr = map[curr][0] if dir2 == "L" else map[curr][1]
    #                 print(z_node, curr, cycle_len, j)
    #             if i not in z_cycles:
    #                 z_cycles[i] = {}
    #             z_cycles[i][z_node] = cycle_len
    #     all_cycles = True
    #     for k in range(len(nodes)):
    #         if k not in z_cycles:
    #             all_cycles = False
    #             break
    #     if all_cycles:
    #         break
    # print(z_cycles)

    i = 0
    # nodes = [nodes[0]]
    walks = [[(node)] for node in nodes]
    repeat = [False for node in nodes]
    while sum([1 for x in repeat if not x]) > 0:
        dir = direction[i]
        i += 1
        i %= len(direction)
        nodes = [(map[curr][0] if dir == "L" else map[curr][1]) for curr in nodes]
        for j in range(len(nodes)):
            if not repeat[j]:
                if nodes[j][-1] == 'Z':
                    walks[j].append((nodes[j], i))
                    repeat[j] = True
                else:
                    walks[j].append((nodes[j]))
    print([len(x) for x in walks])
    ends = [x[-1] for x in walks]
    print(ends)
    for x, _ in ends:
        curr = x
        i = 0
        tot = 0
        while curr != x or tot == 0:
            tot += 1
            dir = direction[i]
            i += 1
            i %= len(direction)
            curr = map[curr][0] if dir == "L" else map[curr][1]
        print(x, tot)
    import math
    print(math.lcm(*[len(x)-1 for x in walks]))
    print(tot2)
    print(len(direction))