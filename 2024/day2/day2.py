import os

basepath = os.path.dirname(os.path.abspath(__file__))

def is_valid(report_i):
    inc = True
    dec = True
    for i in range(len(report_i)-1):
        x = report_i[i]
        y = report_i[i+1]
        if abs(x-y) < 1 or abs(x-y) > 3:
            return False
        if x <= y:
            dec = False
        if y <= x:
            inc = False
    return inc or dec

for filename in ['test_input.txt', 'input.txt']:
    print(filename)
    data = []

    with open(os.path.join(basepath, filename), 'r') as fin:
        for line in fin:
            data.append([int(x) for x in line.strip().split()])

    tot = 0
    tot2 = 0
    for report in data:
        if is_valid(report):
            tot += 1
            tot2 += 1
            continue
        for i in range(len(report)):
            if is_valid(report[:i]+report[i+1:]):
                tot2 += 1
                break

    print(tot)
    print(tot2)
    # There's a way to do this in one pass by just keeping track of the last two numbers, but this was faster to code and works fast enough