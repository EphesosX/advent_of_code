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
    times = [int(x) for x in data[0].split(":")[-1].strip().split()]
    dists = [int(x) for x in data[1].split(":")[-1].strip().split()]

    tot = 1
    for time, distance in zip(times, dists):
        x = time
        y = distance
        # x = time, y = dist, z = charge
        # need (x - z) z > y, xz - z^2 > y, -z^2 + xz - y > 0, z^2 - xz + y < 0
        # z = x/2 +- sqrt(x^2 - 4y) / 2
        ways = 0
        z_min = x/2 - (x**2 - 4 * y) ** 0.5 / 2
        z_min = int(z_min) + 1
        z_max = x/2 + (x**2 - 4 * y) ** 0.5 / 2
        if z_max == int(z_max):
            z_max -= 1
        else:
            z_max = int(z_max)
        ways = z_max - z_min + 1

        tot *= ways
    
    time = int(data[0].split(":")[-1].replace(" ", ""))
    distance = int(data[1].split(":")[-1].replace(" ", ""))
    print(time, distance)
    x = time
    y = distance
    # x = time, y = dist, z = charge
    # need (x - z) z > y, xz - z^2 > y, -z^2 + xz - y > 0, z^2 - xz + y < 0
    # z = x/2 +- sqrt(x^2 - 4y) / 2
    ways = 0
    z_min = x/2 - (x**2 - 4 * y) ** 0.5 / 2
    z_min = int(z_min) + 1
    z_max = x/2 + (x**2 - 4 * y) ** 0.5 / 2
    if z_max == int(z_max):
        z_max -= 1
    else:
        z_max = int(z_max)
    ways = z_max - z_min + 1

    tot2 = ways

    print(tot)
    print(tot2)
