import re


def remove_step_dependence(next_step: str):
    for key in DICT_STEPS:
        list_prev_steps = DICT_STEPS[key]
        for item in list_prev_steps:   # is there better way to delete key from list?
            if item == next_step:
                list_prev_steps.remove(item)

def read_input() -> dict:
    PATTERN = "Step (.) must be finished before step (.)"
    expr = re.compile(PATTERN)
    fh = open("inputs/aoc-7.txt", 'r')
    
    DICT_STEPS = {}

    for line in fh:
        res = expr.search(line)
        groups = res.groups()
        key_before, key_after = [it for it in groups]

        step = DICT_STEPS.get(key_before)
        if step is None:
            DICT_STEPS[key_before] = []

        step = DICT_STEPS.get(key_after)
        if step is None:
            DICT_STEPS[key_after] = step = []
        
        step.append(key_before)
    
    return DICT_STEPS


if __name__ == '__main__':
    DICT_STEPS = read_input()
    # print(DICT_STEPS)

    final_steps = list()
    while DICT_STEPS:    # len(DICT_STEPS) > 0
        '''Find next step to add to the queue'''
        possible_steps = [it for it in DICT_STEPS if DICT_STEPS[it] == []]
        if not possible_steps:
            raise KeyError("no empty steps in dict!!")
        
        next_step = min(possible_steps) # alphabetic comprison (A < B < ... < Z)
        ''' Remove the dependancy of other steps from the removed step '''
        remove_step_dependence(next_step)
        
        final_steps.append(next_step)
        del DICT_STEPS[next_step]

    print(''.join(final_steps))