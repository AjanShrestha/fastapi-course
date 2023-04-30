import pytest
from jose import jwt

from app import schemas
from app.config import settings


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

    login_res = schemas.Token(**res.json())

    assert res.status_code == 200
    assert login_res.token_type == "Bearer"

    payload = jwt.decode(
        login_res.access_token, settings.secret_key, algorithms=[settings.algorithm]
    )
    id = payload.get("user_id")
    assert id == test_user["id"]


@pytest.mark.parametrize(
    "email, password, status_code",
    [
        ("incorrect_email@email.com", "password", 403),
        ("newuser@xyz.com", "incorrect_password", 403),
        (None, "wrongpassword", 422),
        ("newuser@xyz.com", None, 422),
    ],
)
def test_incorrect_login(client, test_user, email, password, status_code):
    res = client.post(
        "/login/",
        data={"username": email, "password": password},
    )

    assert res.status_code == status_code
    # assert res.json().get("detail") == "Invalid credentials"
