import hashlib

import re
word = "#4 @ 184,299: 27x11"
wzor = "#[0-9]+ @ ([0-9]+),([0-9]+): ([0-9]+)x([0-9]+)"
p = re.compile(wzor)

m = p.search(word)
x = m.groups()

(a,b,c,d) = [int(i) for i in x]
print(a,b,c,d)
print(type(a))


# str = "dupa"
#
# result = hashlib.sha1(str.encode())
# out = result.hexdigest()
#
# # printing the equivalent hexadecimal value.
# print("The hexadecimal SHA1: ")
# print(out[0:5])
# print(out[5:])

## zachowane dla ogarniecia eleganckiej skladni jaka generuje liczby w trojkacie
# def write_list(list):
#     print(' '.join([str(item) for item in list]).center(30))
#
# x = 10
# line = [1]
# write_list(line)
# for i in range(int(x) - 1):
#     next_line = [1]
#     for j in range(len(line) - 1):
#         next_line.append(line[j] + line[j + 1])
#     next_line.append(1)
#     line = next_line
#     write_list(line)
#

