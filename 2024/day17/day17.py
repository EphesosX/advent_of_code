import os
import re
import tqdm
import sympy
import sys
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
from utils import *

basepath = os.path.dirname(os.path.abspath(__file__))

for filename in ['test_input.txt','test_input2.txt', 'test_input3.txt','test_input4.txt', 'test_input5.txt', 'test_input6.txt', 'test_input7.txt', 'input.txt']:
    if filename[0] == "t" and filename != 'test_input7.txt':
        continue
    print(filename)
    tot = 0
    tot2 = 0

    lines = []
    grid = []
    with open(os.path.join(basepath, filename), 'r') as fin:
        lines = [x.strip() for x in fin]
        grid = [[x for x in line] for line in lines]

    a = b = c = None
    program = []
    for line in lines:
        if "Register A" in line:
            a = int(line.split(":")[-1].strip())
        if "Register B" in line:
            b = int(line.split(":")[-1].strip())
        if "Register C" in line:
            c = int(line.split(":")[-1].strip())
        if "Program" in line:
            program = [int(x) for x in line.split(":")[-1].strip().split(",")]
    print(a, b, c)
    print(program)
    a_init = a
    b_init = b
    c_init = c

    def combo(x, a, b, c):
        if x >= 0 and x <= 3:
            return x
        if x == 4:
            return a
        if x == 5:
            return b
        if x == 6:
            return c
        raise Exception()
    def xor(x, y):
        result = x ^ y
        return result
    

    # result_map = {}
    # for a_init in range(256):
    #     for c_init in range(256):
            # a = sympy.symbols('a')
    a = a_init
    b = b_init
    c = c_init
    # class BitwiseOr(sympy.Function):
    #     nargs = 2
    #     @classmethod
    #     def eval(cls, x, y):
    #         if x == 0:
    #             return y
    #         if y == 0:
    #             return x
    #         # if x == sympy.Mod(a, 8):
    #         #     return 2 ^ y
    #         print(x, y)
    #         return None
    
    out = []
    inst_ptr = 0
    while inst_ptr < len(program):
        inst = program[inst_ptr]
        op = program[inst_ptr + 1]
        if inst == 0:
            a = a // (2 ** combo(op, a, b, c))
        elif inst == 1:
            # b = BitwiseOr(b, op)
            b = xor(b, op)
        elif inst == 2:
            b = combo(op, a, b, c) % 8
        elif inst == 3:
            print("Jump nz", a)
            if a != 0:
                inst_ptr = op
                continue
        elif inst == 4:
            # b = BitwiseOr(b,c)
            b = xor(b,c)
        elif inst == 5:
            # print('Out', combo(op, a, b, c) % 8)
            out.append(combo(op, a, b, c) % 8)
            # if len(out) > len(program):
            #     break
            # result_map[(a_init, c_init)] = combo(op, a, b, c) % 8
            break
        elif inst == 6:
            b = a // (2 ** combo(op, a, b, c))
        elif inst == 7:
            c = a // (2 ** combo(op, a, b, c))
        inst_ptr += 2
        # if len(out) == len(program) and out[-1] == program[-1]:
        #     break

    # print(result_map)
    # reverse_map = {x: set() for x in result_map.values()}
    # for x,y in result_map.items():
    #     reverse_map[y].add(x)
    # print({x: len(y) for x,y in reverse_map.items()})

    print(out)
    print(a, b, c)
    if out:
        tot = str(",".join([str(x) for x in out]))
    print(tot)

    if filename == "test_input7.txt":
        def try_a(test_a, i):
            print(test_a, i)
            if i < 0:
                print('answer:', test_a * 8)
                return [test_a*8]
            a = program[i]
            return try_a(test_a * 8 + a, i-1)
        
        try_a(0, len(program) - 1)
        continue



    def try_a(test_a, i):
        print(bin(test_a), i)
        if i < 0:
            global tot2
            tot2 = test_a
            return [test_a]
        b = program[i]
        b = b ^ 3
        possible = set()
        for b_test in range(8):
            b_test2 = b_test ^ 2
            # b = b ^ c
            c = (test_a * 8 + b_test) // (2 ** b_test2)
            # c = a // 2**b
            if (b ^ c) % 8 == b_test2:
                possible.add(b_test)
            # b = b ^ 2
        
        # if len(possible) == 1:
        #     # b = a % 8
        #     test_a *= 8
        #     test_a += [x for x in possible][0]
        #     return try_a(test_a, i-1)
        # else:
        results = []
        for x in possible:
            results += try_a(test_a * 8 + x, i-1)
        return results

    try_a(0, len(program) - 1)

    # a = 0
    # for val in program[::-1]:
    #     print(a, val)
    #     b = val # + n * 8
    #     b = b ^ 3
    #     possible = set()
    #     for b_test in range(8):
    #         for n in range(1000):
    #             b_test = b_test ^ 2
    #             # b = b ^ c
    #             c = (a * 8 + b_test) // 2 ** b_test
    #             # c = a // 2**b < 8
    #             if b + n * 8 ^ c == b_test:
    #                 possible.add(b_test ^ 2)
    #             # b = b ^ 2
        
    #     if len(possible) == 1:
    #         # b = a % 8
    #         a *= 8
    #         a += [x for x in possible][0]
    #     else:
    #         print(possible)
    #         raise Exception()

    print(tot2)
    # break

# 444446460 wrong
# 314317163 wrong'

## Feel like this day went awful for me, ended up doing a solution for part 2 hardcoded based on the input
## Got stuck on part 1 for half an hour because I didn't realize the output was supposed to include commas, wasted a lot of time checking implementation
## First approach for part 2 was brute force which failed, then SymPy which went terribly
## Ended up realizing that at each step, the values of b and c get initialized from scratch. So all you need is the last 3 bits of a
## Tried mapping from pairs of (a,c) to possible b values, but didn't realize c could be (much) larger than 8
## Then I tried all possible values in a reverse tree search starting from the halting condition a=0, since you know the printed value of b each time
##   just trying all possible initial values of b to see any that match the final value
## Don't really see how you'd do this one without looking very closely at the input and building the program around that