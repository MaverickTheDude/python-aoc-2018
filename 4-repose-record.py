import re
import copy
SHORTER_MONTHS = [4, 6, 9, 11]

class Entry:
    def __init__(self, minute: int, id: int):
        self.sleep = list()
        self.wake  = list()
        self.guardId = None
        if id == -2:    self.sleep.append(minute)
        elif id == -1:  self.wake.append(minute)
        else:           self.guardId = id

    def append(self, minute: int, id: int):
        if id == -2:    self.sleep.append(minute)
        elif id == -1:  self.wake.append(minute)
        else:           self.guardId = id

    def getSleepMinutes(self) -> list:
        # sleep/wake lists are already sorted
        incidents = len(self.sleep)
        if incidents == 0: return list()
        
        minutesList = list()
        for ind in range(incidents):
            for i in range(self.sleep[ind], self.wake[ind]):
                minutesList.append(i)
        return minutesList

    def countSleep(self) -> int:
        self.sleep.sort()
        self.wake.sort()
        incidents = len(self.sleep)
        if incidents == 0: return 0

        times = [self.wake[i] - self.sleep[i] for i in range(incidents)]
        return sum(times)


    def __str__(self):
        return f"guard {self.guardId}: sleep times {self.sleep}, wake times {self.wake}"

def pickMaxFromDict(dictionary) -> int:
    # returns a key of max value in dictionary.values()
    keyList = list(dictionary.keys())
    valList = list(dictionary.values())
    maxValue = max(valList)
    position = valList.index(maxValue)
    return keyList[position]

def parse(line: str) -> tuple:
    res = expr.search(line)
    groups = res.groups()
    if groups[4] == "Guard": # We know guard id at this day (variable id)
        (month, day, hr, min, id) = [int(elm) for elm in groups if elm != "Guard"]
    else:                    # We know something about sleeping habits (variable min)
        (month, day, hr, min) = [int(elm) for elm in groups[0:4]]
        if groups[4] == "falls": id = -2    # guard falls asleep
        if groups[4] == "wakes": id = -1    # guard wakes up
    if hr == 23:
        if day == 31 or \
           day == 30 and month in SHORTER_MONTHS or \
           day == 28 and month == 2:
            month = month + 1
            day = 1
        else:
            day = day + 1
    return month, day, min, id

if __name__ == "__main__":
    PATTERN = "\[\d+-(\d+)-(\d+) (\d+):(\d+)\] (\w+) \#?(\w+)"
    expr = re.compile(PATTERN)
    fh = open("inputs/aoc-4.txt", 'r')
    Log = dict()
    Registry = list()

    # build up the structure
    for line in fh:
        month, day, min, id = parse(line)
        
        if (month,day) in Log:
            Log[(month,day)].append(min, id)
        else:
            Log[(month,day)] = Entry(min, id)
            Registry.append((month,day))
    Registry.sort() # note: you can compare tuples (pretty intuitively)

    # print the structure contents
    # for elm in Registry:
        # print(elm[0], "-", elm[1], ": ", Log[elm])

    # compute all guard sleep log
    # (create empty dict[min]->incidents)
    sleepLog = {}
    for i in range(60):
        sleepLog[i] = 0

    # (create dict[#guard] -> 'dict[min]->incidents')
    guardLog = {}
    for entry in Log.values():
        guardId = entry.guardId
        if guardId in guardLog:
            minutesList = entry.getSleepMinutes()
            for i in minutesList:
                guardLog[guardId][i] += 1 # each guard's histogram: 00-59: sleep incidence count
        else:
            guardLog[guardId] = copy.deepcopy(sleepLog) # deep or shallow copy is ok (list comprehension would work too)

    # # (pick prime-sleep minute for each guard)
    incidenceLog = dict()
    for guardId in guardLog.keys():
        mostFreqIncident = max(guardLog[guardId].values())
        incidenceLog[guardId] = mostFreqIncident

    guardId = pickMaxFromDict(incidenceLog)
    primeSleptMinute = pickMaxFromDict(guardLog[guardId])
    incidents = guardLog[guardId][primeSleptMinute]

    # primeSleptMinute = guardLog[guardId]
    print(f"Guard #{guardId} got top sleep at minute {primeSleptMinute} ({incidents} times)")
    print(guardId*primeSleptMinute)
