import re
import time
import numpy as np

INITIAL_STATE: str = "..#..###...#####.#.#...####.#..####..###.##.#.#.##.#....#....#.####...#....###.###..##.#....#######"


def read_input() -> dict:
    pattern = "([#,\\.]+) => ([#,\\.])"
    expr = re.compile(pattern)
    fh = open("inputs/aoc-12.txt", 'r')

    rules_dict = dict()

    for line in fh:
        res = expr.search(line)
        groups = res.groups()
        rule, outcome = [it for it in groups]
        rules_dict[rule] = outcome

    return rules_dict


def get_new_state(state_old: str, rules_: dict) -> str:
    # boundary case for the begining
    state_new: str = ''
    if state_old[0:2] == '#.':
        state_new = '#'
        get_new_state.origin += 1

    # regular logic
    for it, _ in enumerate(state_old):
        state_new += apply_rule(state_old, it, rules_)

    # boundary case for the end
    if state_old[-2:] == '.#' or state_old[-2:] == '##':
        state_new += '#'

    # remove leading empty spots
    remove_cnt = 0
    for i in range(len(state_new)):
        if state_new[i] == '.':
            remove_cnt += 1
        else:
            break
    state_new = state_new[remove_cnt:]
    get_new_state.origin -= remove_cnt

    return state_new


def apply_rule(state: str, location: int, rules_: dict) -> str:
    if location < 2:
        prefix = '.' * (2 - location)
        suffix = ''
        start: int = 0
        end = location + 3
    elif location > len(state) - 3:
        prefix = ''
        suffix = '.' * (location - len(state) + 3)  # (3 - (len(state) - location))
        start: int = location - 2
        end = len(state)
    else:
        prefix = ''
        suffix = ''
        start = location - 2
        end = location + 3

    local_state: str = prefix + state[start:end] + suffix
    return rules_[local_state]


def calculate_sum(state: str) -> int:
    sum = 0
    for i in range(len(state)):
        if state[i] == '#':
            sum += i - get_new_state.origin
    return sum

# initialization of 'static' variable
get_new_state.origin = 0

if __name__ == "__main__":
    rules = read_input()
    plants_length = len(INITIAL_STATE)

    start = time.time()
    new_state = INITIAL_STATE
    oldsum = calculate_sum(new_state)
    for i in range(400):
        new_state = get_new_state(new_state, rules)
        # diff = calculate_sum(new_state) - oldsum
        # print(f"{new_state} \t at {get_new_state.origin} \t iter: {i+1} \t sum: {calculate_sum(new_state)} \t diff: {diff}")
        # oldsum = calculate_sum(new_state)

    elapsed = time.time() - start
    print(f'elapsed: {elapsed:.3f} s')

    print(new_state)
    sum = calculate_sum(new_state)
    print(f'origin: {get_new_state.origin}, total length: {len(new_state)}, sum: {sum}')

    p = np.polyfit([200, 400], [11962, 22562], 1)
    value = np.polyval(p, 5e10)
    print(f"value = {np.ceil(value)}")
