import re

CHAR_OFFSET = 64
INT_NUM_WORKERS = 5
INT_SEC_PENALTY = 60


class Workload:
    def __init__(self) -> None:
        self.__list_worker_pool: list = INT_NUM_WORKERS * [None]
        self.__list_worktime: list = INT_NUM_WORKERS * [1]
        self.__time_elapsed: int = 0
        self.__signal_state_change: bool = False

    def is_active(self) -> bool:
        for worker in self.__list_worker_pool:
            if worker is not None:
                return True
        return False

    def count_idle_workers(self):
        x = [it for it in self.__list_worker_pool if it is None]
        return len(x)

    def assign_tasks(self, task_pool: list) -> None:
        for it, worker in enumerate(self.__list_worker_pool):
            if not task_pool:
                break
            if not worker:
                next_step = min(task_pool)
                self.__list_worker_pool[it] = next_step
                task_pool = remove_from_list(next_step, task_pool)

    def __advance(self) -> str:
        step_to_delete = "EMPTY"
        for it, worker in enumerate(self.__list_worker_pool):
            if not worker:
                continue
            time_to_finish = INT_SEC_PENALTY + ord(worker) - CHAR_OFFSET
            if self.__list_worktime[it] == time_to_finish:
                if self.__signal_state_change:
                    raise ValueError("we assume only one element to remove at a time")
                step_to_delete = worker
                self.__list_worker_pool[it] = None
                self.__list_worktime[it] = 1
                self.__signal_state_change = True
            else:
                self.__list_worktime[it] += 1
        
        self.__time_elapsed += 1        
        return step_to_delete

    def advance_2next_state(self) -> None:
        while not self.__signal_state_change:
            step_to_delete = self.__advance()
        self.__signal_state_change = False
        self.__clear_finished_step(step_to_delete, dict_steps)
        Steps_Order.append(step_to_delete)
    
    def __clear_finished_step(self, step_to_delete: str, dict_steps: dict):
        ''' Remove the dependancy of other steps from the removed step '''
        for key in dict_steps:
            list_prev_steps = dict_steps[key]
            dict_steps[key] = remove_from_list(step_to_delete, list_prev_steps)
        
    def __iter__(self):
        return WorkerIterator(self)

# https://thispointer.com/python-how-to-make-a-class-iterable-create-iterator-class-for-it/
class WorkerIterator:
   ''' Iterator class '''
   def __init__(self, workload: Workload):
       # workload object reference
       self._workload = workload
       # member variable to keep track of current index
       self._index = 0
   def __next__(self):
       ''''Returns the next value from workload object's lists '''
       # note: we explicitly get private member of Workload via name mangling
       if self._index < len(self._workload._Workload__list_worker_pool) :
           result = (f"worker id: {self._index}", self._workload._Workload__list_worker_pool[self._index])
           self._index += 1
           return result
       # End of Iteration
       raise StopIteration

# A nice way to delete key from list via list comprehension
def remove_from_list(key, list_: list) -> list:
    result = list()
    result[:] = [val for val in list_ if val != key]
    return result

def read_input() -> dict:
    PATTERN = "Step (.) must be finished before step (.)"
    expr = re.compile(PATTERN)
    fh = open("inputs/aoc-7.txt", 'r')
    
    dict_steps = {}

    for line in fh:
        res = expr.search(line)
        groups = res.groups()
        key_before, key_after = [it for it in groups]

        step = dict_steps.get(key_before)
        if step is None:
            dict_steps[key_before] = []

        step = dict_steps.get(key_after)
        if step is None:
            dict_steps[key_after] = step = []
        
        step.append(key_before)
    
    return dict_steps


if __name__ == '__main__':
    dict_steps = read_input()
    # print(dict_steps)

    obj_workload = Workload()
    Steps_Order = list()
    cnt = 0
    while dict_steps:    # len(dict_steps) > 0
        '''Find next step to add to the queue and remove them from the dict_steps'''
        possible_steps = [it for it in dict_steps if dict_steps[it] == []]
        possible_steps.sort()
        n_items = obj_workload.count_idle_workers()
        possible_steps = possible_steps[:n_items]
        for step_to_delete in possible_steps:
            del dict_steps[step_to_delete]

        '''Assign tasks to the worload and iterate over 
            additional tasks until they're finished '''
        obj_workload.assign_tasks(possible_steps)

        '''Iterate over workload until single task is finished'''
        print(f"step: {cnt}, time elapsed: {obj_workload._Workload__time_elapsed}")
        cnt += 1
        for x in obj_workload:
            print(x)

        obj_workload.advance_2next_state()

    while obj_workload.is_active():
        obj_workload.advance_2next_state()

    print(''.join(Steps_Order))
    print(f"time elapsed is {obj_workload._Workload__time_elapsed}")
