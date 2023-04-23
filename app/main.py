import time

import psycopg
from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from psycopg.rows import dict_row
from random import randrange

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True


while True:
    try:
        conn = psycopg.connect(
            "host=localhost dbname=fastapi user=postgres password=postgres",
            row_factory=dict_row,
        )
        cursor = conn.cursor()
        print("Database connection was successful")
        break
    except Exception as error:
        print("Connection to database failed")
        print("Error: %s" % error)
        time.sleep(2)


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


def find_index_post(id: int):
    for index, post in enumerate(my_posts):
        if post["id"] == id:
            return index
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
    posts = cursor.execute("""SELECT * FROM posts """).fetchall()
    return {"data": posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
# extract all the params from the request body,
# convert it into python dictionarym, and
# store it inside variable paylopad
def create_posts(post: Post):
    # parameterized and sanitize
    # security: make it safe from SQL injection
    new_post = cursor.execute(
        """INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""",
        (post.title, post.content, post.published),
    ).fetchone()
    # commit to save it in the database
    conn.commit()
    return {"data": new_post}


# path parameter
@app.get("/posts/{id}")
# convert the id into int as default type is string
def get_post(id: int):
    post = cursor.execute("""SELECT * FROM posts WHERE id=%s""", (str(id),)).fetchone()
    if not post:
        raise (
            HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Post with id: {id} was not found",
            )
        )
    return {"post_detail": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    deleted_post = cursor.execute(
        """DELETE FROM posts WHERE id=%s RETURNING *""", (str(id),)
    ).fetchone()
    conn.commit()

    if deleted_post is None:
        raise (
            HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Post with id: {id} was not found",
            )
        )

    # Normally we don't return anything, on delete success
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    updated_post = cursor.execute(
        """UPDATE posts SET title=%s, content=%s, published=%s WHERE id=%s RETURNING *""",
        (post.title, post.content, post.published, str(id)),
    ).fetchone()
    conn.commit()

    if updated_post is None:
        raise (
            HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Post with id: {id} was not found",
            )
        )

    return {"data": updated_post}
