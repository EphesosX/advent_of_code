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
    for line in data:
        digits = [int(x) for x in line.split()]
        grid = [digits]
        while len(set(grid[-1])) > 1:
            next_line = []
            for i in range(len(grid[-1]) - 1):
                next_line.append(grid[-1][i+1]-grid[-1][i])
            grid.append(next_line)
        k = grid[-1][0]
        k2 = k
        for i in range(len(grid) - 2, -1, -1):
            k += grid[i][-1]
            k2 = grid[i][0] - k2
        tot += k
        tot2 += k2

    print(tot)
    print(tot2)
