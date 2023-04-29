from fastapi.testclient import TestClient

from app import schemas
from app.main import app


client = TestClient(app)


def test_root():
    res = client.get("/")
    print(res.json().get("message"))
    assert res.status_code == 200
    assert res.json().get("message") == "Hello World!"


def test_create_user():
    res = client.post(
        "/users", json={"email": "newuser@xyz.com", "password": "password"}
    )
    new_user = schemas.UserOut(**res.json())
    assert new_user.email == "newuser@xyz.com"
    assert res.status_code == 201
