data = []

with open('input.txt', 'r') as fin:
# with open('test_input.txt', 'r') as fin:
    for line in fin:
        data.append(line.strip())


tot = 0
tot2 = 0
grid = []
for line in data:
    grid.append([x for x in line])

grid2 = []
grid3 = []

part_nums = []
for i in range(len(grid)):
    grid2.append([False for x in grid[i]])
    grid3.append([False for x in grid[i]])
    for j in range(len(grid[i])):
        if grid[i][j] != ".":
            try:
                int(grid[i][j])
            except:
                grid2[i][j] = True
            if grid[i][j] == "*":
                grid3[i][j] = True

all_gears = []

for i in range(len(grid)):
    j = 0
    while j < len(grid[i]):
        try:
            digit = int(grid[i][j])
            part_num = digit
            has_symbol = False
            gears = set()
            while True:
                adj = []
                for x in range(i-1, i+2):
                    for y in range(j-1, j+2):
                        try:
                            grid[x][y]
                            adj.append((x,y))
                        except:
                            pass
                                    
                for x, y in adj:
                    if grid2[x][y]:
                        has_symbol = True
                    if grid3[x][y]:
                        gears.add((x, y))
                j += 1
                try:
                    digit = int(grid[i][j])
                    part_num = 10 * part_num + digit
                except:
                    break
            if has_symbol:
                part_nums.append(part_num)
                all_gears.append(gears)
        except:
            j += 1
        

for part_num in part_nums:
    tot += part_num

counts = {}
for gear_set in all_gears:
    for gear in gear_set:
        counts[gear] = counts.get(gear, 0) + 1

for gear in counts:
    if counts[gear] == 2:
        mult = 1
        for gear_set, part_num in zip(all_gears, part_nums):
            if gear in gear_set:
                mult *= part_num
        tot2 += mult

print(tot)
print(tot2)