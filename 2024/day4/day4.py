import os
import re

basepath = os.path.dirname(os.path.abspath(__file__))


for filename in ['test_input.txt', 'input.txt']:
    print(filename)
    tot = 0
    tot2 = 0

    with open(os.path.join(basepath, filename), 'r') as fin:
        lines = [line.strip() for line in fin]
        segments = [line for line in lines]
        for j in range(len(lines[0])):
            col = ""
            for i in range(len(lines)):
                col += lines[i][j]
            segments.append(col)
        for s in range(len(lines) + len(lines[0])):
            diag = ""
            diag2 = ""
            for i in range(len(lines)):
                for j in range(0, len(lines[0])):
                    if i+j == s:
                        diag += lines[i][j]
                    if i + len(lines[0]) - 1 - j == s:
                        diag2 += lines[i][j]
            segments.append(diag)
            segments.append(diag2)

        for segment in segments:
            for x in re.findall(r"XMAS", segment):
                tot += 1
            for x in re.findall(r"XMAS"[::-1], segment):
                tot += 1

        for i in range(len(lines)-2):
            for j in range(len(lines[0])-2):
                grid = lines[i][j:j+3] + lines[i+1][j:j+3]+ lines[i+2][j:j+3]
                for pattern in [r"M.S.A.M.S", r"M.M.A.S.S", r"S.S.A.M.M", r"S.M.A.S.M"]:
                    for x in re.findall(pattern, grid):
                        tot2 += 1


    print(tot)
    print(tot2)
    # break

# started 5 minutes late
# was thinking of marking all locations of A which matched the pattern MAS, and then checking for overlaps, but there's only 4 possible variations of the pattern here so this was easier
