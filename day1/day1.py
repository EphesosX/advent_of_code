data = []

with open('input.txt', 'r') as fin:
# with open('test_input.txt', 'r') as fin:
    for line in fin:
        data.append(line.strip().split()[0])

key = {"one":1, "two":2, "three":3, "four": 4, "five":5, "six":6, "seven":7, "eight":8, "nine":9}

tot = 0
for line in data:
    digits = []
    i = 0
    # for i in range(len(line)):
    while i < len(line):
        # print(i)
        char = line[i]
        try:
            digits.append(int(char))
        except:
            for x,y in key.items():
                if line[i:i+len(x)] == x:
                    digits.append(y)
                    # i += len(x) - 1
                    break
            pass
        i += 1
    # print(digits)
    # print(digits[0]*10+digits[-1])
    tot += digits[0]*10+digits[-1]

print(tot)

# 54678
# 54547
# 54170
# 54676