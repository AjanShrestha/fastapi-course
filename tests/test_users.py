import pytest

from app import schemas
from .database import client, session


@pytest.fixture
def test_user(client):
    user_data = {"email": "newuser@xyz.com", "password": "password"}
    res = client.post("/users/", json=user_data)

    assert res.status_code == 201
    new_user = res.json()
    new_user["password"] = user_data["password"]

    return new_user


def test_root(client):
    res = client.get("/")
    print(res.json().get("message"))
    assert res.status_code == 200
    assert res.json().get("message") == "Hello World!"


def test_create_user(client):
    res = client.post(
        "/users/", json={"email": "newuser@xyz.com", "password": "password"}
    )
    assert res.status_code == 201
    new_user = schemas.UserOut(**res.json())
    assert new_user.email == "newuser@xyz.com"


def test_login_user(client, test_user):
    res = client.post(
        "/login/", data={"username": "newuser@xyz.com", "password": "password"}
    )

    assert res.status_code == 200
