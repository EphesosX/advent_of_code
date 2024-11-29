import os
basepath = os.path.dirname(os.path.abspath(__file__))

def get_neighbors2(i, j, m, n):
    nbrs = []
    if i > 0:
        nbrs.append((i-1,j))
    if i < m-1:
        nbrs.append((i+1,j))
    if j > 0:
        nbrs.append((i,j-1))
    if j < n-1:
        nbrs.append((i,j+1))
    return nbrs

for filename in ['test_input.txt', 'input.txt']:
    print(filename)
    data = []

    with open(os.path.join(basepath, filename), 'r') as fin:
        for line in fin:
            data.append(line.strip())


    tot = 0
    tot2 = 0
    grid = []
    for line in data:
        grid.append([x for x in line])
    
    def expand(grid):
        empty_rows = []
        empty_cols = []
        for i in range(len(grid)):
            if sum([1 if x != '.' else 0 for x in grid[i]]) == 0:
                empty_rows.append(i)
        for j in range(len(grid[0])):
            is_empty = True
            for i in range(len(grid)):
                if grid[i][j] != '.':
                    is_empty = False
            if is_empty:
                empty_cols.append(j)
        # for i in empty_rows[::-1]:
        #     grid.insert(i, ['.']*len(grid[0]))
        # for j in empty_cols[::-1]:
        #     for row in grid:
        #         row.insert(j, '.')
        return empty_rows, empty_cols
    
    empty_rows, empty_cols = expand(grid)

    # for x in grid:
    #     for y in x:
    #         print(y, end='')
    #     print()
    # break

    stars = []
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == "#":
                x = i
                for empty_row in empty_rows:
                    if i > empty_row:
                        x += 999999
                y = j
                for empty_col in empty_cols:
                    if j > empty_col:
                        y += 999999
                stars.append((x,y))
    print(stars)

    for i in range(len(stars)):
        x, y = stars[i]
        for j in range(len(stars)):
            if j > i:
                x2, y2 = stars[j]
                tot += abs(x-x2) + abs(y-y2)



    print(tot)
    
    print(tot2)
