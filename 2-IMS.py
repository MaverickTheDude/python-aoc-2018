def calculateSymbols(string: str) -> tuple:
    a = 0
    b = 0
    cont = dict()
    for x in string:
        if x in cont:   cont[x] += 1
        else:           cont[x] = 1
    if 2 in cont.values():  a = 1
    if 3 in cont.values():  b = 1
    return a, b


def compare(string: str) -> str:
    n = len(string)
    for word in idSet:
        cnt = 0
        index = None
        for it in range(n):
            if string[it] != word[it]:
                cnt += 1
                index = it
            if cnt > 1: break
        if cnt == 1:
            outStr = ''.join([string[i] for i in range(n) if i != index])
            return outStr
    return ""

A = 0
B = 0
fh = open("inputs/aoc-2.txt", 'r')
idSet = set()
box = ""
for line in fh:
    (a, b) = calculateSymbols(line)
    if box == "" and len(idSet) > 0:
        box = compare(line)
    idSet.add(line)
    A += a
    B += b
fh.close()

print("checksum = ", A*B)
print("box name: ", box)