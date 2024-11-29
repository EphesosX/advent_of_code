for filename in ['test_input.txt', 'input.txt']:
    print(filename)
    data = []

    with open(filename, 'r') as fin:
        for line in fin:
            data.append(line.strip())


    tot = 0
    tot2 = 0
    winners = []
    hands = []
    for line in data:
        parts = line.split(":")[-1]
        winners.append([int(x) for x in parts.strip().split("|")[0].strip().split()])
        hands.append([int(x) for x in parts.strip().split("|")[1].strip().split()])
        n_matches = len([x for x in winners[-1] if x in hands[-1]])
        if n_matches > 0:
            tot += 2 ** (n_matches - 1)
    
    copies = {}
    for i, winner in enumerate(winners):
        copies[i] = copies.get(i, 0) + 1
        hand = hands[i]
        n_matches = len([x for x in winner if x in hand])
        if n_matches > 0:
            for j in range(i+1, i+n_matches+1):
                if j < len(winners):
                    copies[j] = copies.get(j, 0) + copies[i]
    if len(copies) < 10:
        print(copies)
    tot2 = sum(copies.values())

    print(tot)
    print(tot2)
