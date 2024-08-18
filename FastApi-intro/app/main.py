from fastapi import FastAPI, Response, status, HTTPException
from typing import Union
from pydantic import BaseModel
from typing import Optional
from random import randrange
# from fastapi.params import Body


# https://fastapi.tiangolo.com/#example
app  = FastAPI()

my_posts = [{'title': 'post 1', 'content': 'wtf', 'id': 1}, \
            {'title': 'post 2', 'content': '666', 'id': 2}]

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def create_post(payload: Post):  # payload: dict = Body(...)
    post_dict = payload.dict()
    post_dict['id'] = randrange(0, 1000000)
    my_posts.append(post_dict)
    # print(post_dict)
    return {"data": my_posts}

@app.get("/posts")
async def get_posts():
    return {"data": my_posts}

@app.get("/posts/{id}")
def get_post(id: int): #  response: Response
    post = [x for x in my_posts if x['id']==id]
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                      detail=f"post {id=} not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"data": f"post {id=} not found"}
    else:
        post = post[0]
    return {"data": f"this is post {post=}"}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    for it, post in enumerate(my_posts):
        if post['id'] == id:
            my_posts.pop(it)
            return Response(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"post {id=} not found, can't delete")

@app.put('/posts/{id}')
def update_posts(id: int, post_new: Post):
    for it, post in enumerate(my_posts):
        if post['id'] == id:
            post_tmp = post_new.dict()
            post_tmp['id'] = id
            my_posts[it] = post_tmp
            return {"message": f"updated post {id=}", "data": post_tmp}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"post {id=} not found, can't update")

@app.get("/")
async def read_root():
    return {"Hello": "World", "wtf:": "xddd"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

# def main():
#     pass

# if __name__ == "main":
#     main()