for filename in ['test_input.txt', 'input.txt']:
    print(filename)
    data = []

    with open(filename, 'r') as fin:
        for line in fin:
            data.append(line.strip())


    tot = 0
    tot2 = 0
    seeds = [int(x) for x in data[0].split(":")[-1].strip().split()]
    i = 2
    maps = {}
    while i < len(data):
        word = data[i].split()[0]
        x, z, y = word.split("-")
        maps[(x, y)] = {}
        i += 1
        while i < len(data) and data[i]:
            dest_start, src_start, length = [int(x) for x in data[i].split()]
            maps[(x, y)][(src_start, length)] = dest_start
            i += 1
        i += 1
    
    key = 'seed'
    curr = seeds
    while key != 'location':
        new_curr = []
        next_key = [y for x, y in maps if x == key][0]
        curr_map = maps[(key, next_key)]
        for x in curr:
            found = False
            for src_start, length in curr_map:
                if x >= src_start and x < src_start + length:
                    new_curr.append(curr_map[(src_start, length)] + x - src_start)
                    found = True
                    break
            if not found:
                new_curr.append(x)
        key = next_key
        curr = new_curr
    
    tot = min(new_curr)

    seeds2 = [(seeds[2*i], seeds[2*i+1]) for i in range(len(seeds) // 2)]
    print(seeds2)

    
    key = 'seed'
    curr = seeds2
    while key != 'location':
        new_curr = []
        next_key = [y for x, y in maps if x == key][0]
        curr_map = maps[(key, next_key)]
        i = 0
        while i < len(curr):
            x, y = curr[i]
            i += 1
            found = False
            for src_start, length in curr_map:
                if x+y >= src_start and x < src_start + length:
                    if x >= src_start:
                        if x+y <= src_start + length:
                            new_curr.append((curr_map[(src_start, length)] + x - src_start, y))
                            found = True
                            break
                        else:
                            new_curr.append((curr_map[(src_start, length)] + x - src_start, length - x + src_start))
                            y -= length - x + src_start
                            x = src_start + length
                    else:
                        if x+y <= src_start + length:
                            new_curr.append((curr_map[(src_start, length)], x+y-src_start))
                            y = src_start - x
                        else:
                            new_curr.append((curr_map[(src_start, length)], length))
                            curr.append((src_start+length, x + y - src_start-length))
                            y = src_start - x
            if not found:
                new_curr.append((x, y))
        key = next_key
        curr = new_curr
        if filename != "input.txt":# or key == 'soil':
            print(key)
            print(curr_map)
            print(new_curr)

    # if filename != "input.txt":
        # print(new_curr)
    tot2 = min([x for x, y in new_curr])
    print(tot)
    print(tot2)
