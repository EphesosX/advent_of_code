import os
import re
import tqdm

basepath = os.path.dirname(os.path.abspath(__file__))

for filename in ['test_input.txt', 'input.txt']:
    print(filename)
    tot = 0
    tot2 = 0

    lines = []
    equations = []
    with open(os.path.join(basepath, filename), 'r') as fin:
        for line in fin:
            lhs = int(line.split(":")[0])
            rhs = [int(x) for x in line.split(":")[1].strip().split(" ")]
            equations.append((lhs, rhs))
    # print(equations)

    for lhs, rhs in equations:
        values = set()
        values.add(rhs[0])
        for x in rhs[1:]:
            new_values = set()
            for y in values:
                new_values.add(y + x)
                new_values.add(y * x)
                new_values.add(int(str(y)+str(x)))
            values = new_values
        if lhs in values:
            tot += lhs

    print(tot)
    print(tot2)
    # break

## super fast day, took longer to write the parsing code than the solution itself
## evaluation could be a bit faster if you stopped when the new value becomes larger than the test value, just because all 3 operations are monotonic increasing
