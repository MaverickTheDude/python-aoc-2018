
def iterate():
    freq = 0
    # big brain time: list has linear complexity so the iterations take more time
    # dictionary has constant look-up complexity so all iterations took a second
    # freq_list = [] # list, a no-go
    freq_list = {}
    it = 1
    while True:
        for f in changes:
            freq += f
            if freq in freq_list: return freq
            #freq_list.append(freq)
            #freq_list.sort() # sorting doesn't help
            freq_list[freq] = freq
        print("iteracja: ", it)
        it += 1


changes = []
fh = open("inputs/aoc-1.txt", 'r')
for line in fh:
    changes.append(int(line.strip()))
fh.close()

x = iterate()

print("zdublowana czestotliwosc: ", x)