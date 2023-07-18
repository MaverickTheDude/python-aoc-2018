import re


SAFE_DISTANCE = 10000


def read_input() -> set:
    PATTERN = "(\d+), (\d+)"
    expr = re.compile(PATTERN)
    fh = open("inputs/aoc-6.txt", 'r')
    
    POINTS_SET = set()

    for line in fh:
        res = expr.search(line)
        groups = res.groups()
        x, y = [int(it) for it in groups]
        POINTS_SET.add( (x, y) )
    
    return POINTS_SET

def get_boundary() -> tuple:
    any_point = next(iter(POINTS_SET))
    min_x = any_point[0]
    max_x = any_point[0]
    min_y = any_point[1]
    max_y = any_point[1]
    for point in POINTS_SET:
        if point[0] < min_x: min_x = point[0]
        if point[0] > max_x: max_x = point[0]
        if point[1] < min_y: min_y = point[1]
        if point[1] > max_y: max_y = point[1]
    
    return (min_x, max_x, min_y, max_y)

def manhattan(point_A: tuple, point_B: tuple) -> int:
    result = abs(point_A[0] - point_B[0]) + abs(point_A[1] - point_B[1])
    return result

# Picks closest point to the given querry point from the POINTS_SET
def find_closest(query_point: tuple) -> tuple:
    best_value = 9999999 # arbitrary large number
    for point in POINTS_SET:
        new_value = manhattan(query_point, point)
        if new_value == best_value:
            chamption = None
        if new_value < best_value:
            best_value = new_value
            chamption = point

    return chamption

def calculate_total_distance(querry_point: tuple) -> int:
    distance = 0
    for point in POINTS_SET:
        distance += manhattan(point, querry_point)

    return distance

if __name__ == "__main__":
    POINTS_SET = read_input()

    min_x, max_x, min_y, max_y = get_boundary()

    # iterate over the finite segment boundary and check which labels are infinite 
    # question: how to nicely combine these loops together?
    infinite_labels = set()
    for x in range(min_x, max_x+1):
        for y in (min_y, max_y):
            region_label = find_closest( (x,y) )
            infinite_labels.add(region_label)
    for y in range(min_y, max_y+1):
        for x in (min_x, max_x):
            region_label = find_closest( (x,y) )
            infinite_labels.add(region_label)

    # iterate over finite segment and count all labels
    regions = dict() # key: label, ie. input point, value: # of points closest to it
    for x in range(min_x+1, max_x):
        for y in range(min_y+1, max_y):
            region_label = find_closest( (x,y) )
            if region_label is None: continue
            if region_label not in regions:
                regions[region_label] = 1
            else:
                regions[region_label] += 1

    valList = list(regions.values())
    maxValue = max(valList)
    print(f"largest finite area size: {maxValue}")

# PART B
    NsafeRegions = 0
# note: we separately checked that at the boundary distance is greater than SAFE_DISTANCE
#       so only inner region must be concerned
    for x in range(min_x, max_x+1):
        for y in range(min_y, max_y+1):
            distance = calculate_total_distance( (x,y) )
            if distance < SAFE_DISTANCE:
                NsafeRegions += 1

    print(f"Number of safe regions: {NsafeRegions}")
