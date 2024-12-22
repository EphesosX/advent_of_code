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
    # if filename[0] == "t":
    #     continue
    tot = 0
    tot2 = 0

    lines = []
    grid = []
    with open(os.path.join(basepath, filename), 'r') as fin:
        lines = [x.strip() for x in fin]
        grid = [[x for x in line] for line in lines]

    numbers = [int(x) for x in lines]

    def mix(x,y):
        return x ^ y
    
    def prune(x):
        return x % 16777216

    def secret(x):
        y = x * 64
        z = prune(mix(x,y))
        w = z // 32
        v = prune(mix(z,w))
        a = v * 2048
        return prune(mix(v,a))

    prices = []
    for number in numbers:
        prices_i = [number % 10]
        for i in range(2000):
            number = secret(number)
            prices_i.append(number % 10)
        prices.append(prices_i)
        tot += number
    price_changes = [[x[i+1]-x[i] for i in range(len(x)-1)] for x in prices]

    # x = prices[0]
    # for i in range(len(x)-10):
    #     if tuple(x[1000:1010]) == tuple(x[i:i+10]):
    #         print(i)
    # break

    # best_sale = 0
    # def get_combos():
    #     for c1 in range(-9,9)[::-1]:
    #         for c2 in range(-9,9):
    #             for c3 in range(-9,9):
    #                 for c4 in range(-9,9):
    #                     yield (c4,c3,c2,c1)
    
    # for pattern in tqdm.tqdm(get_combos(), total=19**4):
    #     sale = 0
    #     for price, price_change in zip(prices, price_changes):
    #         # print(price[0])
    #         for i in range(len(price_change)-4):
    #             if tuple(price_change[i:i+4]) == pattern:
    #                 sale += price[i+4]
    #                 # if pattern == (-2,1,-1,3):
    #                 #     print(sale)
    #                 #     print(tuple(price_change[i:i+4]), pattern)
    #                 break
    #     if sale > best_sale:
    #         best_sale = max(sale, best_sale)
    #         print(best_sale)
    #     # if pattern == (-2,1,-1,3):
    #     #     print(sale, best_sale)
    

    # print(sale)
    sales = {}
    for price, price_change in zip(prices, price_changes):
        # print(price[0])
        sales_i = {}
        for i in range(len(price_change)-4):
            pattern =  tuple(price_change[i:i+4])
            if pattern not in sales_i:
                sales_i[pattern] = price[i+4]
        for x, y in sales_i.items():
            if x not in sales:
                sales[x] = 0
            sales[x] += y
    tot2 = max(sales.values())

    # print(sales[(-2,1,-1,3)])
    print(tot)
    print(tot2)
    # break

# x << 6
# x |= x
# x %= 2**24
#    b_i = { x_i ^ x_i-6   i >= 6
#            x_i           i < 6
# x >> 5
# x |= x
# x %= 2**24
#    b_i = { x_i ^ x_i-6   i > 19
#            x_i ^ x_i-6 ^ x_i+5 ^ x_i-1    19 >= i >= 6
#            x_i ^ x_i+5 ^ x_i-1            6 > i >= 1
#            x_i ^ x_i+5                    i == 0
# x << 11
# x |= x
# x %= 2**24
#    b_i = {y_i ^ y_i-11   i >= 11
#           y_i            i < 11
#        = {x_i ^ x_i-11 ^ x_i-17 ^ x_i-12    i > 19
#           x_i ^ i+5 ^ i-1 ^ i-11 ^ i-12       19 >= i > 11
#           x_i ^ i+5 ^ i-1 % x_i-11     i == 11
#            x_i ^ x_i-6 ^ x_i+5 ^ x_i-1    11 > i >= 6
#            x_i ^ x_i+5 ^ x_i-1            6 > i >= 1
# 	   x^i ^ x_i+5                    i == 0

# 1599 wrong
    
## part 1 pretty much just brute force, though I wasted a lot of time looking for some kind of bit pattern to speed things up
## part 2 tried to brute force and tqdm realized it'd take 50+ hours
## kept searching for patterns in the secret numbers before I gave up and turned to optimizing
## realized that I could do it in linear time by just iterating over price changes and summing
## after that my error was adding multiple prices per pattern instead of just the first one, otherwise went smoothly