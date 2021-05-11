import re
N = 1000


# translate 2d coordinate onto 1d; column-major order
# x - go right, y - go down
def idx(x, y):
    return x + y*N


def coords(line):
    m = expr.search(line)
    groups = m.groups()
    (i, x, y, m, n) = [int(i) for i in groups]  # list comprehension on tuple
    return i, x, y, m, n


PATTERN = "#([0-9]+) @ ([0-9]+),([0-9]+): ([0-9]+)x([0-9]+)"
expr = re.compile(PATTERN)


# create map between field id and # of times it duplicates
fieldMap = {}
fh = open("inputs/aoc-3.txt", 'r')
for line in fh:
    (i, x, y, m, n) = coords(line)
    for i in range(x, x+m):
        for j in range(y, y+n):
            ind = idx(i, j)
            if ind in fieldMap:
                fieldMap[ind] += 1
            else:
                fieldMap[ind] = 1

# rerun the calculations to figure out which claim doesn't overlap
fh.seek(0)
for line in fh:
    overlap = False
    (id, x, y, m, n) = coords(line)
    for i in range(x, x+m):
        for j in range(y, y+n):
            ind = idx(i, j)
            print(fieldMap[ind])
            if fieldMap[ind] > 1:
                overlap = True
                break
        if overlap: break
    if overlap: continue
    claim = id
    break
fh.close()

doubledElms = [i for i in fieldMap if fieldMap[i] > 1]  # list comprehension on dict
print("doubled elements: ", len(doubledElms))
print("single claim: ", claim)
