import os
basepath = os.path.dirname(os.path.abspath(__file__))

for filename in ['test_input.txt', 'input.txt']:
    print(filename)
    data = []

    with open(os.path.join(basepath, filename), 'r') as fin:
        for line in fin:
            data.append(line.strip())


    def to_int(x):
        return 10 if x == 'T' else 0 if x == 'J' else 12 if x == 'Q' else 13 if x=='K' else 14 if x == 'A' else int(x)

    tot = 0
    tot2 = 0
    ranked_hands = []
    for line in data:
        cards = line.split()[0]
        bid = int(line.split()[1])
        counts = {}
        for x in cards:
            counts[x] = counts.get(x, 0) + 1
        if 'J' in counts:
            n_j = counts['J']
            if n_j in [1, 2, 3, 4]:
                del counts['J']
                x = max([x for x in counts], key=lambda x: (counts[x], to_int(x)))
                counts[x] += n_j

        is_full_house = 3 in counts.values() and 2 in counts.values()
        is_hand = [x in counts.values() for x in range(1, 6)]
        is_hand.insert(3, is_full_house)
        is_two_pair = len([x for x in counts.values() if x == 2]) == 2
        is_hand.insert(2, is_two_pair)
        ranked_hands.append(([1 if x else 0 for x in is_hand[::-1]], [to_int(x) for x in cards], bid))
    for i, hand in enumerate(sorted(ranked_hands, key=lambda x: (x[0], x[1]))):
        if filename[0]=='t' or True:
            print(hand, i+1)
        tot += (i+1) * hand[-1]

    print(tot)
    print(tot2)
    # 253702560
    # 253254392
