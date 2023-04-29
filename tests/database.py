import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config import settings
from app.database import Base, get_db
from app.main import app

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
