import math


x = list()

def foo():
    xxx += 1 # this breaks the code, but can is there a way to modify global variable in python 
    print(f"x = {xxx}")

if __name__ == "__main__":
    print(sum(x))


# # >python: select interpreter
# import signal  
# import sys  
# import asyncio  
# import aiohttp  
# import json

# loop = asyncio.get_event_loop()  
# client = aiohttp.ClientSession(loop=loop)

# async def get_json(client, url):  
#     async with client.get(url) as response:
#         assert response.status == 200
#         return await response.read()

# async def get_reddit_top(subreddit, client):  
#     data1 = await get_json(client, 'https://www.reddit.com/r/' + subreddit + '/top.json?sort=top&t=day&limit=5')

#     j = json.loads(data1.decode('utf-8'))
#     for i in j['data']['children']:
#         score = i['data']['score']
#         title = i['data']['title']
#         link = i['data']['url']
#         print(str(score) + ': ' + title + ' (' + link + ')')

#     print('DONE:', subreddit + '\n')

# def signal_handler(signal, frame):  
#     loop.stop()
#     client.close()
#     sys.exit(0)

# signal.signal(signal.SIGINT, signal_handler)

# asyncio.ensure_future(get_reddit_top('python', client))  
# asyncio.ensure_future(get_reddit_top('programming', client))  
# asyncio.ensure_future(get_reddit_top('compsci', client))  
# loop.run_forever()