from typing import Optional
from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


# In-memory storage for posts
my_posts = [
    {"title": "Sample Post", "content": "This is post 1", "id": 1},
    {"title": "Favorite food", "content": "Momo", "id": 2},
]


def find_post(id: int):
    for post in my_posts:
        if post["id"] == id:
            return post
    return None


# Path Operation / Route
# Decorator converts the function into a path operation
# Makes it an API that can be called
# decorator - object.HTTPFunction(Params)
# Path operation converts function into API
@app.get("/")
def root():
    # Converts it to JSON
    return {"message": "Hello World!"}


@app.get("/posts")
def get_posts():
    return my_posts


@app.post("/posts")
# extract all the params from the request body,
# convert it into python dictionarym, and
# store it inside variable paylopad
def create_posts(post: Post):
    # Pydantic model to Python dict
    post_dict = post.dict()
    post_dict["id"] = randrange(1, 9999999)
    my_posts.append(post_dict)
    return {"data": post_dict}


# path parameter
@app.get("/posts/{id}")
# convert the id into int as default type is string
def get_post(id: int):
    post = find_post(id)
    return {"post_detail": post}
