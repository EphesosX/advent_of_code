data = []

with open('input.txt', 'r') as fin:
# with open('test_input.txt', 'r') as fin:
    for line in fin:
        data.append(line.strip())

limits = {"red": 12, "green": 13, "blue": 14}

tot = 0
tot2 = 0
for line in data:
    game_num = int(line.split(":")[0].split()[-1])

    maxs = {"red": 0, "green": 0, "blue": 0}
    
    hands = line.split(":")[-1].split(";")
    fail = False
    for hand in hands:
        tokens = hand.strip().split(",")
        
        for token in tokens:
            num = int(token.split()[0])
            color = token.split()[-1]
            if num > limits[color]:
                fail = True
            maxs[color] = max(maxs[color], num)
    if not fail: 
        tot += game_num
    tot2 += maxs["red"] * maxs["green"] * maxs["blue"]

print(tot)
print(tot2)