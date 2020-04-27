from urllib.request import urlopen
from bs4 import BeautifulSoup
import ssl
import re


def gettags(url, ctx):
    html = urlopen(url, context=ctx).read()
    soup = BeautifulSoup(html, "html.parser")
    tags = soup('a')
    return tags

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

#url = 'http://py4e-data.dr-chuck.net/known_by_Fikret.html'
url = 'http://py4e-data.dr-chuck.net/known_by_Saphyre.html'
tags = gettags(url, ctx)
posSet = 18
bounces = 7

for i in range(1, bounces+1):
    pos = 1
    for tag in tags:
        if pos < posSet:
            pos += 1
            continue
        print(tag.get('href', None))
        url = tag.get('href', None)
        tags = gettags(url, ctx)
        name = re.findall('_by_(.+).html', url)
        if len(name) > 1: print('fixme')
        break
print(name[0])