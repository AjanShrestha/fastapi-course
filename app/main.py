import time
import psycopg
from psycopg.rows import dict_row
from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel

from .db import get_db_conn_string

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


while True:
    try:
        cursor = psycopg.connect(
            get_db_conn_string(),
            row_factory=dict_row,
        )
        # cursor = conn.cursor()
        print("Database connection was successful")
        break
    except Exception as error:
        print("Connection to database failed")
        print("Error: ", error)
        time.sleep(2)


@app.get("/")
def root():
    return {"message": "Hello World!!"}


@app.get("/posts")
def get_posts():
    posts = cursor.execute("""SELECT * FROM posts""").fetchall()
    return {"data": posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    new_post = cursor.execute(
        """INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""",
        (post.title, post.content, post.published),
    ).fetchone()
    cursor.commit()
    return new_post


@app.get("/posts/{id}")
def get_post(id: int):
    post = cursor.execute(
        """SELECT * FROM posts WHERE id = %s""", (str(id),)
    ).fetchone()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} was not found",
        )
    return {"data": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    deleted_post = cursor.execute(
        """DELETE FROM posts WHERE id = %s RETURNING *""", (str(id),)
    ).fetchone()

    if not deleted_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} was not found",
        )
    cursor.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    updated_post = cursor.execute(
        """UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
        (post.title, post.content, post.published, str(id)),
    ).fetchone()
    if not updated_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} was not found",
        )
    cursor.commit()
    return {"data": updated_post}
