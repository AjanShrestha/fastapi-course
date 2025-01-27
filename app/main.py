from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


class Counter:
    __count = 0

    @staticmethod
    def get_new_id():
        Counter.__count += 1
        return Counter.__count


my_posts = [
    {
        "title": "title of post 1",
        "content": "content of post 1",
        "id": Counter.get_new_id(),
    },
    {"title": "favourite food", "content": "I like pizza", "id": Counter.get_new_id()},
]


def find_post(id):
    return [post for post in my_posts if post["id"] == id][0]


def find_index_post(id):
    for index, post in enumerate(my_posts):
        if post["id"] == id:
            return index
    raise ValueError("No id found")


@app.get("/")
def root():
    return {"message": "Hello World!!"}


@app.get("/posts")
def get_posts():
    return {"data": my_posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(new_post: Post):
    my_posts.append(new_post.model_dump() | {"id": Counter.get_new_id()})
    return my_posts[-1]


@app.get("/posts/{id}")
def get_post(id: int):
    try:
        return find_post(id)
    except IndexError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} was not found",
        )


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    try:
        index = find_index_post(id)
        my_posts.pop(index)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} was not found",
        )


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    try:
        index = find_index_post(id)
        post_dict = post.model_dump()
        post_dict["id"] = id
        my_posts[index] = post_dict
        return {"data": post_dict}
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} was not found",
        )
