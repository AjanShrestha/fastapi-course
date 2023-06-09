import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app import models
from app.config import settings
from app.database import Base, get_db
from app.main import app
from app.oauth2 import create_access_token

SQLACHEMY_DATABASE_URL = f"{settings.database}://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test"

# engine - responsible for SQLAlchemy to connect to the database
engine = create_engine(SQLACHEMY_DATABASE_URL)

# talk to the database via session
TestingSessionLocal = sessionmaker(autoflush=False, bind=engine)


@pytest.fixture
def session():
    # run our code before we run our test
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
        # run our code after our test finishes
    finally:
        db.close()


@pytest.fixture
def client(session):
    # Dependency
    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)


@pytest.fixture
def test_user(client):
    user_data = {"email": "newuser@xyz.com", "password": "password"}
    res = client.post("/users/", json=user_data)

    assert res.status_code == 201
    new_user = res.json()
    new_user["password"] = user_data["password"]

    return new_user


@pytest.fixture
def test_user2(client):
    user_data = {"email": "seconduser@xyz.com", "password": "password"}
    res = client.post("/users/", json=user_data)

    assert res.status_code == 201
    new_user = res.json()
    new_user["password"] = user_data["password"]

    return new_user


@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": test_user["id"]})


@pytest.fixture
def authorized_client(client, token):
    client.headers = {**client.headers, "Authorization": f"Bearer {token}"}
    return client


@pytest.fixture()
def test_posts(session, test_user, test_user2):
    posts_data = [
        {"title": "1st title", "content": "1st content", "owner_id": test_user["id"]},
        {"title": "2nd title", "content": "2nd content", "owner_id": test_user["id"]},
        {"title": "3rd title", "content": "3rd content", "owner_id": test_user["id"]},
        {"title": "4th title", "content": "4th content", "owner_id": test_user2["id"]},
    ]

    def create_post_model(post):
        return models.Post(**post)

    post_map = map(create_post_model, posts_data)
    posts = list(post_map)
    session.add_all(posts)
    # session.add_all(
    #     [
    #         models.Post(
    #             title="1st title", content="1st content", owner_id=test_user["id"]
    #         ),
    #         models.Post(
    #             title="2nd title", content="2nd content", owner_id=test_user["id"]
    #         ),
    #         models.Post(
    #             title="3rd title", content="3rd content", owner_id=test_user["id"]
    #         ),
    #     ]
    # )
    session.commit()

    return posts
