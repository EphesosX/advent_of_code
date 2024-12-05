import os
import re

basepath = os.path.dirname(os.path.abspath(__file__))


for filename in ['test_input.txt', 'input.txt']:
    print(filename)
    tot = 0
    tot2 = 0

    rules = []
    pages = []
    with open(os.path.join(basepath, filename), 'r') as fin:
        lines = [line.strip() for line in fin]
        for line in lines:
            if "|" in line:
                rules.append([int(x) for x in line.split("|")])
            elif "," in line:
                pages.append([int(x) for x in line.split(",")])
    # print(rules)
    # print(pages)

    for page in pages:
        correct = True
        for x, y in rules:
            if x in page and y in page:
                for a in page:
                    if a == y:
                        correct = False
                        break
                    elif a == x:
                        break
        if correct:
            tot += page[len(page)//2]
        else:
            while not correct:
                correct = True
                for x, y in rules:
                    if x in page and y in page:
                        for a in page:
                            if a == y:
                                correct = False
                                tmp = page.index(x)
                                page[page.index(y)] = x
                                page[tmp] = y
                                break
                            elif a == x:
                                break
            tot2 += page[len(page) // 2]

    print(tot)
    print(tot2)
    # break

## Finally started on time for once. Got a bit held up on trying to define a custom sort comparator before realizing that I could just write my own sort faster
## Not sure what sorting algorithm this is, but as long as your rules are consistent (no loops) it should at least terminate
## After some googling, looks like it's a topological sort of some kind? There's definitely possible sets with multiple valid orders, but I assume those aren't in the given input
