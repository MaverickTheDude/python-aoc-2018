import hashlib

str = "dupa"

result = hashlib.sha1(str.encode())
out = result.hexdigest()

# printing the equivalent hexadecimal value.
print("The hexadecimal SHA1: ")
print(out[0:5])
print(out[5:])

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

