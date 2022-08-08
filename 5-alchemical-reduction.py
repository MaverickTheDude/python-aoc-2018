def polymerMatch(x: str, y: str) -> bool:
    if x.casefold() == y.casefold() and x is not y:
        return True
    else: return False

def readFile(fh) -> list:
    polymer = list()
    previous = '?'

    while True:
        current = fh.read(1)
        if not current:
            break

        if polymerMatch(previous, current):
            polymer.pop()
            if len(polymer) == 0:
                previous = '?'
            else:
                previous = polymer[-1]
        else:
            polymer.append(current)
            previous = current

    return polymer

def truncate(polymer: list) -> list:
    polymerOut = list()
    previous = '?'

    for current in polymer:

        if polymerMatch(previous, current):
            polymerOut.pop()
            if len(polymerOut) == 0: 
                previous = '?'
            else:
                previous = polymerOut[-1]
        else:
            polymerOut.append(current)
            previous = current
    return polymerOut

def removeSymbol(eraser: str, polymer: list) -> list:
    polymerOut = list()
    for symbol in polymer:
        if symbol != eraser and symbol != eraser.capitalize():
            polymerOut.append(symbol)
    return polymerOut

def main(fh):
    # part A: single sweep of the input file
    polymer = readFile(fh)
    naturalSize = len(polymer)

    # part B: create score dictionary and all symbols that appear in polymer
    scoreDict = dict()
    symbolList = list()
    for s in polymer:
        if s.casefold() not in symbolList:
            symbolList.append(s.casefold())

    # simulate all possibilities
    for symbol in symbolList:
        polymerCopy = removeSymbol(symbol, polymer)
        polymerCopy = truncate(polymerCopy)
        scoreDict[symbol] = len(polymerCopy)

    keyList = list(scoreDict.keys())
    valList = list(scoreDict.values())
    minValue = min(valList)
    position = valList.index(minValue)
    bestSymbol = keyList[position]

    for key in scoreDict:
        print(f'symbol {key} reduces polymer to the following length: {scoreDict[key]}')

    print('task A: size of the polymer = ', naturalSize)
    print('task B: best symbol to optimize is', bestSymbol, '(score = ', scoreDict[bestSymbol], ')')


if __name__ == "__main__":
    fh = open("inputs/aoc-5.txt", 'r')
    main(fh)
    fh.close()