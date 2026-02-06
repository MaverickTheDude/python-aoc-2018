import re
import matplotlib.pyplot as plt

class Point:
    def __init__(self, x: str, y: str, vel_x: str, vel_y: str):
        self.x = int(x)
        self.y = int(y)
        self.vel_x = int(vel_x)
        self.vel_y = int(vel_y)

    def advance(self, times: int = 1) -> None:
        for i in range(times):
            self.x += self.vel_x
            self.y += self.vel_y


def read_input() -> list:
    pattern = "position=<\\s?(-?\\d+),\\s+(-?\\d+)> velocity=<\\s?(-?\\d),\\s+(-?\\d)>"
    expr = re.compile(pattern)
    fh = open("inputs/aoc-10.txt", 'r')

    all_points = list()

    for line in fh:
        res = expr.search(line)
        groups = res.groups()
        x, y, vel_x, vel_y = [it for it in groups]
        all_points.append(Point(x, y, vel_x, vel_y))

    return all_points


def draw_points(all_points: list, ax) -> None:
    for point in all_points:
        ax.plot(point.x, point.y, 'o', markersize=1, color='black')
    plt.show()


if __name__ == "__main__":
    all_points = read_input()

    fig = plt.figure()
    fig.patch.set_facecolor('white')

    multiplier = 1
    offset = 10_117
    for p in all_points: p.advance(offset)

    plt.ion()
    for it in range(1):
        plt.clf()
        ax = plt.gca()
        ax.title.set_text("time = {} s".format(it*multiplier + offset))
        draw_points(all_points, ax)

        plt.pause(10)
        for p in all_points: p.advance(multiplier)
        # After vertical offset: RGRKHKNA

