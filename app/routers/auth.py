from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session


from .. import database, models, schemas, utils

router = APIRouter(tags=["Authentication"])


@router.post("/login/")
def login(user_credentials: schemas.UserLogin, db: Session = Depends(database.get_db)):
    user = (
        db.query(models.User)
        .filter(models.User.email == user_credentials.email)
        .first()
    )

    if not (user and utils.verify(user_credentials.password, user.password)):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid credentials"
        )

    # create a token
    # return token
    return {"token": "example token"}
