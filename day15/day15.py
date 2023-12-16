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

for filename in ['test_input.txt', 'input.txt']:
    print(filename)
    data = []

    with open(os.path.join(basepath, filename), 'r') as fin:
        for line in fin:
            data.append(line.strip())

    tot = 0
    tot2 = 0
    for line in data:
        break
    parts = line.split(",")
    for part in parts:
        curr = 0
        for x in part:
            curr += ord(x)
            curr *= 17
            curr %= 256
        # print(part, curr)
        tot += curr

    boxes = [[] for x in range(256)]
    
    for part in parts:
        if '=' in part:
            label = part.split('=')[0]
            lens_n = int(part.split('=')[1])
        elif '-' in part:
            label = part.split('-')[0]
        curr = 0
        for x in label:
            curr += ord(x)
            curr *= 17
            curr %= 256
        
        if '=' in part:
            box_i = boxes[curr]
            changed = False
            for i, lens in enumerate(box_i):
                if label == lens[0]:
                    lens[1] = lens_n
                    changed = True
            if not changed:
                box_i.append([label, lens_n])
            
        elif '-' in part:
            box_i = boxes[curr]
            to_remove = None
            for i, lens in enumerate(box_i):
                if label == lens[0]:
                    to_remove = lens
            if to_remove is not None:
                box_i.remove(to_remove)

    for i in range(256):
        box_i = boxes[i]
        for j, lens in enumerate(box_i):
            tot2 += (i+1) * (j+1) * lens[1]
    

    print(tot)
    print(tot2)
    # break