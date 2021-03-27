import heapq
from typing import Tuple, List, TypeVar

T = TypeVar('T')


class PriorityQueue:
    def __init__(self):
        self.elements: List[Tuple[float, T]] = []

    def empty(self) -> bool:
        return not self.elements

    def put(self, item: T, priority: float):
        heapq.heappush(self.elements, (priority, item))

    def get(self) -> T:
        return heapq.heappop(self.elements)[1]


def dijkstra_search(graph, start=(0, 0)):
    goal = graph.goal
    frontier = PriorityQueue()
    frontier.put(start, 0)
    came_from = {}  # inna inicjalizacja slownika
    cost_so_far = dict()
    came_from[start] = None
    cost_so_far[start] = 0
    solutions = []

    while not frontier.empty():
        current = frontier.get()

        if current == goal:
            solutions.append( graph_ex1.reconstruct_path(came_from) )
            break
# case gdy chcemy zwrocic rownie optymalne rozwiazania (to do)
            # if dijkstra_search.best_sum == 0:       # one-time: set 'static' variable
            #     dijkstra_search.best_sum = cost_so_far[current]
            # elif cost_so_far[current] < dijkstra_search.best_sum:
            #     break
            # current = frontier.get()

        for next in graph.neighbors(current):
            new_cost = cost_so_far[current] + graph.cost(next)
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                priority = new_cost
                frontier.put(next, priority)
                came_from[next] = current

    return solutions


# initialization of 'static' variable
dijkstra_search.best_sum = 0


def line2list(line):
    list_out = []
    for char in line:
        if char == ' ': continue
        list_out.append(int(char))
    return list_out


class graph:
    def __init__(self):
        self.values = []
        self.pos = []

        # get graph weights from input
        fh = open("Dijkstra/" + FILE, 'r')
        for line in fh:
            numbers = line2list(line.strip())
            self.values.append(numbers)
        fh.close()
        self.height = len(self.values)
        self.values.append([0])

        self.goal = (self.height, 0)
        # initialize graph topology
        for x in range(self.height):
            for y in range(0, x + 1):
                self.pos.append((x, y))
        self.pos.append(self.goal)

    def cost(self, index):
        return self.values[index[0]][index[1]]

    def neighbors(self, node):
        if node[0] == self.height - 1:
            return [self.goal]
        dirs = [(1, 0), (1, 1)]
        result = []
        for dir in dirs:
            result.append( (node[0] + dir[0], node[1] + dir[1]) )
        return result

    def reconstruct_path(self, came_from: dict):
        start = (0, 0)
        current = self.goal
        path = []
        vals = []
        total_cost = 0
        while current != start:
            value = self.cost(current)
            path.append(current)
            total_cost += value
            vals.append(value)
            current = came_from[current]
        path.append(start)
        path.reverse()
        path.pop()

        value = self.cost(start)
        total_cost += value
        vals.append(value)
        vals.reverse()
        vals.pop()

        return {"values": vals, "cost": total_cost, "path": path}


# FILE = '1-very_easy.txt'
# FILE = '2-easy.txt'
FILE = '3-medium.txt'

graph_ex1 = graph()
solution = dijkstra_search(graph_ex1)

print("Liczba rozwiazan: ", len(solution))

for sol in solution:
    print(sol["path"])
    print(sol["values"])
    print(sol["cost"])
    # print("\n")

answer = list(map(str, sol["values"]))
answer = ''.join(answer)
print(answer)