
def fun():
    # print(f"x from fun: {x}")
    x = 3
    print(f"x from fun #2: {x}")


if __name__ == "__main__":

    x = [1, 2, 3, 4, 5]
    z = x
    z[1] = 10
    print(z is x)
    x = []
    print(z is x)

    # z = []

    print(z)


# import re

# def parse(line: str) -> tuple:
#     res = expr.search(line)
#     groups = res.groups()
#     (m, d, h, min, x, id) = [elm for elm in groups]  # list comprehension on tuple
#     if x == "Guard": id = int(id)
#     else: id = -1
#     return int(m), int(d), int(h), int(min), id

# PATTERN = "\[\d+-(\d+)-(\d+) (\d+):(\d+)\] (\w+) \#?(\w+)"
# expr = re.compile(PATTERN)


# fh = open("inputs/aoc-4.txt", 'r')
# for line in fh:
#     m, d, h, min, id = parse(line)
#     print(m,d,h,min,id)

