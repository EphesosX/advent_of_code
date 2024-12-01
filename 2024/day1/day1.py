import os

basepath = os.path.dirname(os.path.abspath(__file__))

for filename in ['test_input.txt', 'input.txt']:
    print(filename)
    data = []

    with open(os.path.join(basepath, filename), 'r') as fin:
        for line in fin:
            data.append([int(x) for x in line.strip().split()])

    loc_1 = sorted([x[0] for x in data])
    loc_2 = sorted([x[1] for x in data])
    print(sum([abs(x-y) for x,y in zip(loc_1, loc_2)]))
    print(sum([x * len([y for y in loc_2 if y==x]) for x in loc_1]))

## Not sure if there's a more efficient way to do part 1 if sorting the lists took too long. 
## It's essentially Wasserstein distance so probably not faster than O(N log(N))
## Part 2 could have been done in O(N) time by creating the map from digits to counts in one pass on the second list, 
## then iterating on the first.