import numpy as np

SERIAL_NUMBER: int = 4151
# SERIAL_NUMBER: int = 42


# Hack for slightly more efficient matrix traversal: artifically put new column in place of the discarded one
def moveNode(array: np.ndarray[int], root_x: int, root_y: int):
    tmp: np.array = (calculatePowerLevel(root_x+2, root_y),
                     calculatePowerLevel(root_x+2, root_y+1),
                     calculatePowerLevel(root_x+2, root_y+2))
    array[:, moveNode.row] = tmp
    moveNode.row = moveNode.row + 1 if moveNode.row < 2 else 0


def calculateNode(root_x: int, root_y: int) -> np.ndarray[int]:
    node: np.ndarray = np.zeros((3, 3), dtype=int)
    for it_x, x in enumerate(range(root_x, root_x+3)):
        for it_y, y in enumerate(range(root_y, root_y+3)):
            node[it_y, it_x] = calculatePowerLevel(x, y)

    return node


def calculatePowerLevel(x: int, y: int) -> int:
    rackId: int = x + 10
    powerLevel: int = (rackId * y + SERIAL_NUMBER) * rackId
    return (powerLevel % 1000) // 100 - 5  # get the value from hundreds


# initialization of 'static' variable
moveNode.row = 0

if __name__ == "__main__":
    maxNodeValue: int = 0
    maxNodeCoords: tuple = ()

    for y in range(1, 299):
        node = calculateNode(1, y)
        for x in range(2, 299):
            moveNode(node, x, y)
            tmp = calculateNode(x, y)
            if (newMaxNodeValue := sum(sum(node))) > maxNodeValue:
                maxNodeValue = newMaxNodeValue
                maxNodeCoords = (x, y)

    print(f"max node value = {maxNodeValue}")
    print(f"max node coords = {maxNodeCoords}")
    print(f"max node = \n {calculateNode(maxNodeCoords[0], maxNodeCoords[1])}")


    # node1 = calculateNode(1,61)
    # for i in range(2, 23):
    #     moveNode(node1, i, 61)
    #     if i > 19:
    #         print(f"({i},{61}): \n {node1}")

    # print(f"node = \n {calculateNode(21,61)}")
    # print(f"sum = {sum(sum(calculateNode(21,61)))}")
