import os
import re
import tqdm
import sys
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
from utils import *

basepath = os.path.dirname(os.path.abspath(__file__))

for filename in ['test_input.txt', 'input.txt']:
    print(filename)
    tot = 0
    tot2 = 0

    lines = []
    grid = []
    with open(os.path.join(basepath, filename), 'r') as fin:
        lines = [x.strip() for x in fin]
        grid = [[x for x in line] for line in lines]

    groups = []
    group = None
    for line in lines:
        if 'Button A' in line:
            x_shift = int(line.split("X+")[1].split(",")[0].strip())
            y_shift = int(line.split("Y+")[1].strip())
            group = (x_shift, y_shift)
        elif 'Button B' in line:
            x_shift = int(line.split("X+")[1].split(",")[0].strip())
            y_shift = int(line.split("Y+")[1].strip())
            group = (group, (x_shift, y_shift))
        elif 'Prize' in line:
            x_loc = int(line.split("X=")[1].split(",")[0].strip())
            y_loc = int(line.split("Y=")[1].strip())
            groups.append(((x_loc,y_loc), group))
            group = None

    # print(groups)

    # |x1 x2| a = px
    # |y1 y2| b = py
    # a, b = [[x1, x2], [y1, y2]] ^-1 [px, py]

    for group in groups:
        prize, buttons = group
        prize = [ x for x in prize]
        prize[0] = prize[0] + 10000000000000
        prize[1] = prize[1] + 10000000000000
        button_a, button_b = buttons
        det = button_a[0] * button_b[1] - button_a[1] * button_b[0]
        if det == 0:
            raise Exception()
        divides = True
        a = button_b[1] * prize[0] - button_b[0] * prize[1]
        b = button_a[0] * prize[1] - button_a[1] * prize[0]
        if a % det != 0:
            divides = False
        if b % det != 0:
            divides = False
        if not divides:
            continue
        a = a // det
        b = b // det
        tot += 3 * a+b
                
    print(tot)
    print(tot2)
    # break

## took me embarassingly long to remember and type 2x2 inverse formulas
## was expecting to maybe handle a determinant of 0, but didn't have to in the end
## would be a bit tougher since you need to check gcd, but then it's just a change-making problem with 2 coins
## part 2 was super easy since the linear algebra doesn't care how big the values are, guessing they expected an iterative search for part 1