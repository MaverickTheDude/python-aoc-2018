from fastapi import FastAPI
from typing import Union


# https://fastapi.tiangolo.com/#example
app  = FastAPI()



@app.get("/")
async def read_root():
    return {"Hello": "World", "wtf:": "xddd"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

def main():
    pass

if __name__ == "main":
    main()