import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app import models, schemas
from app.config import settings
from app.database import Base, get_db
from app.main import app

SQLACHEMY_DATABASE_URL = f"{settings.database}://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test"

# engine - responsible for SQLAlchemy to connect to the database
engine = create_engine(SQLACHEMY_DATABASE_URL)

# talk to the database via session
TestingSessionLocal = sessionmaker(autoflush=False, bind=engine)


# Dependency
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture
def client():
    # run our code before we run our test
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield TestClient(app)
    # run our code after our test finishes


def test_root(client):
    res = client.get("/")
    print(res.json().get("message"))
    assert res.status_code == 200
    assert res.json().get("message") == "Hello World!"


def test_create_user(client):
    res = client.post(
        "/users", json={"email": "newuser@xyz.com", "password": "password"}
    )
    new_user = schemas.UserOut(**res.json())
    assert new_user.email == "newuser@xyz.com"
    assert res.status_code == 201
