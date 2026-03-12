import re

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
    for i in range(get_new_state.origin):
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


# initialization of 'static' variable
get_new_state.origin = 0

if __name__ == "__main__":
    rules = read_input()
    plants_length = len(INITIAL_STATE)

    new_state = INITIAL_STATE
    for _ in range(20):
        new_state = get_new_state(new_state, rules)
        print(f'{new_state} \t at {get_new_state.origin}')

    sum = 0
    for i in range(len(new_state)):
        if new_state[i] == '.':
            continue
        sum += i - get_new_state.origin
        print(f'# at {i}')


    print(new_state)
    print(f'origin: {get_new_state.origin}, total length: {len(new_state)}, sum: {sum}')

