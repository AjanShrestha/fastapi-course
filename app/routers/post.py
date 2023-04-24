from typing import List

from fastapi import APIRouter, Depends, Response, status, HTTPException
from sqlalchemy.orm import Session


from ..database import get_db
from .. import models, schemas

router = APIRouter()


@router.get("/posts", response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db)):
    # posts = cursor.execute("""SELECT * FROM posts """).fetchall()

    posts = db.query(models.Post).all()
    return posts


@router.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
# extract all the params from the request body,
# convert it into python dictionarym, and
# store it inside variable paylopad
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db)):
    # # parameterized and sanitize
    # # security: make it safe from SQL injection
    # new_post = cursor.execute(
    #     """INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""",
    #     (post.title, post.content, post.published),
    # ).fetchone()
    # # commit to save it in the database
    # conn.commit()

    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    # we cannot set RETURNING in SQLAlchemy hence refresh with the updated id
    db.refresh(new_post)

    return new_post


# path parameter
@router.get("/posts/{id}", response_model=schemas.Post)
# convert the id into int as default type is string
def get_post(id: int, db: Session = Depends(get_db)):
    # post = cursor.execute("""SELECT * FROM posts WHERE id=%s""", (str(id),)).fetchone()

    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise (
            HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Post with id: {id} was not found",
            )
        )

    return post


@router.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    # deleted_post = cursor.execute(
    #     """DELETE FROM posts WHERE id=%s RETURNING *""", (str(id),)
    # ).fetchone()
    # conn.commit()

    post = db.query(models.Post).filter(models.Post.id == id)

    if post.first() is None:
        raise (
            HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Post with id: {id} was not found",
            )
        )

    post.delete(synchronize_session=False)
    db.commit()

    # Normally we don't return anything, on delete success
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/posts/{id}", response_model=schemas.Post)
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db)):
    # updated_post = cursor.execute(
    #     """UPDATE posts SET title=%s, content=%s, published=%s WHERE id=%s RETURNING *""",
    #     (post.title, post.content, post.published, str(id)),
    # ).fetchone()
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)

    if post_query.first() is None:
        raise (
            HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Post with id: {id} was not found",
            )
        )

    post_query.update(post.dict(), synchronize_session=False)
    db.commit()

    return post_query.first()
