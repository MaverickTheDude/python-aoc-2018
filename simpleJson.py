import urllib.request
import json

url = 'http://py4e-data.dr-chuck.net/comments_448600.json'
uh = urllib.request.urlopen(url)
data = uh.read()

info = json.loads(data)
comments = info['comments']

sum = 0
for com in comments:
    x = com['count']
    sum += x

print('User count:', len(comments))
print('sum:', sum)