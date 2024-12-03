import os
import re

basepath = os.path.dirname(os.path.abspath(__file__))


for filename in ['test_input.txt', 'input.txt']:
    print(filename)
    tot = 0
    tot2 = 0

    with open(os.path.join(basepath, filename), 'r') as fin:
        line = fin.read()
        segments = line.split("do()")
        for segment in segments:
            segment = segment.split("don't()")[0]
            for x in re.findall(r"mul\((\d{1,3}),(\d{1,3})\)", segment):
                # print(x[0])
                # print(x[1])
                a = int(x[0])
                b = int(x[1])
                tot += a * b


    print(tot)
    print(tot2)
    # break

# 29728992 fail
# Started 12 minutes late on this one because I wasn't watching the time, so it actually took me closer to 10 minutes
# could have been a bit faster if I hadn't messed up read() vs. readline()