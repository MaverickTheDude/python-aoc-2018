import numpy as np
import time


SERIAL_NUMBER: int = 4151

# AAR (after action report): xy indexing in np.meshgrid is equivalent to x-negative-y grid (the same as in current task)
# (In fact, I would call it intuitively 'ij', but meybe I don't get the convention right)
# The results will be identical to the following loop (notice gridtmp[i,j] which is asymetrical to (x,y))
# for y in range(1, 31): --> i
#   for x in range(1, 31): --> j
#         gridtmp[y-1, x-1] = calculatePowerLevel(x, y)

# Return entire 300x300 grid in one call (calculatePowerLevel trivially vectorized)
def buildGrid() -> np.ndarray[int]:
    xs = np.arange(1, 301)
    ys = np.arange(1, 301)

    # Create 2D grids via broadcasting
    X, Y = np.meshgrid(xs, ys, indexing='xy')
    grid = calculatePowerLevel(X, Y)
    return grid


# Optimized for single vectorized calculation over the grid and looping over the results (not that significantly quicker, though)
def solveGridB(window_size: int, optimalWindowSize_: int, maxNodeCoords_: tuple, maxNodeValue_: int) -> tuple:
    xlimit = 302 - window_size
    for y in range(1, xlimit):
        i = y-1
        for x in range(1, xlimit):
            j = x - 1
            if (newMaxNodeValue := sum(sum(grid[i:i+window_size, j:j+window_size]))) > maxNodeValue_:
                maxNodeValue_ = newMaxNodeValue
                maxNodeCoords_ = (x, y)
                optimalWindowSize_ = window_size
                # print(f"better node found: ws: {window_size}, val: {maxNodeValue_}, coords: {maxNodeCoords_}")
    return optimalWindowSize_, maxNodeCoords_, maxNodeValue_

# More naive approach for part A: initially assumed the size of the grid will be x1000
def solveGridA(window_size: int, optimalWindowSize_: int, maxNodeCoords_: tuple, maxNodeValue_: int) -> tuple:
    xlimit = 302 - window_size
    for y in range(1, xlimit):
        node = calculateNode(1, y, window_size)
        for x in range(2, xlimit):
            moveNode(node, x, y, window_size)
            if (newMaxNodeValue := sum(sum(node))) > maxNodeValue_:
                maxNodeValue_ = newMaxNodeValue
                maxNodeCoords_ = (x, y)
                optimalWindowSize_ = window_size
                print(f"better node found: ws: {window_size}, val: {maxNodeValue_}, coords: {maxNodeCoords_}")
    return optimalWindowSize_, maxNodeCoords_, maxNodeValue_

# Hack for slightly more efficient matrix traversal: artifically put new column in place of the discarded one
def moveNode(array: np.ndarray[int], root_x: int, root_y: int, windowSize: int):
    offset: int = windowSize - 1
    tmp: np.array = np.empty(windowSize, dtype=int)
    for i in range(windowSize):
        tmp[i] = calculatePowerLevel(root_x + offset, root_y + i)
    array[:, moveNode.row] = tmp
    moveNode.row = moveNode.row + 1 if moveNode.row < offset else 0


def calculateNode(root_x: int, root_y: int, ws: int) -> np.ndarray[int]:
    node: np.ndarray = np.zeros((ws, ws), dtype=int)
    for it_x, x in enumerate(range(root_x, root_x + ws)):
        for it_y, y in enumerate(range(root_y, root_y + ws)):
            node[it_y, it_x] = calculatePowerLevel(x, y)

    return node


def calculatePowerLevel(x: np.ndarray | int, y: np.ndarray | int) -> np.ndarray | int:
    rackId: int = x + 10
    powerLevel: int = (rackId * y + SERIAL_NUMBER) * rackId
    return (powerLevel % 1000) // 100 - 5  # get the value from hundreds


# initialization of 'static' variable
moveNode.row = 0

if __name__ == "__main__":
    optimalWindowSize: int = 0
    maxNodeCoords: tuple = ()
    maxNodeValue: int = 0
    grid = buildGrid()

    start = time.perf_counter()
    for windowsSize in range(2, 20):
        t1 = time.perf_counter()
        # optimalWindowSize, maxNodeCoords, maxNodeValue = solveGridA(windowsSize, optimalWindowSize, maxNodeCoords, maxNodeValue)
        optimalWindowSize, maxNodeCoords, maxNodeValue = solveGridB(windowsSize, optimalWindowSize, maxNodeCoords, maxNodeValue)
        t2 = time.perf_counter()
        print(f"window size {windowsSize} calculated in {t2 - t1:.2f}s (total: {t2 - start:.2f}s)")

    print(f"max node value = {maxNodeValue}")
    print(f"max node coords = {maxNodeCoords}, ws = {optimalWindowSize}")
    print(f"max node = \n {calculateNode(maxNodeCoords[0], maxNodeCoords[1], 3)}")
