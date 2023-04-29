from app import schemas

from .database import client, session


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
