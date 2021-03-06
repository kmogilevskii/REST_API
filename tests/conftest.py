import pytest
from app import models
from app.main import app
from app.config import settings
from sqlalchemy import create_engine
from app.database import get_db, Base
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from app.oath2 import create_access_token


SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# default fixture scope is a function so they're gonna run before each function
@pytest.fixture()
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture()
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    return TestClient(app)


@pytest.fixture()
def create_user(client):
    user_data = {
        "email": "konstest@gmail.com",
        "password": "password123"
    }
    res = client.post("/users/", json=user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user


@pytest.fixture()
def token(create_user):
    return create_access_token(data={"user_id": create_user["id"]})

@pytest.fixture()
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }

    return client


@pytest.fixture()
def create_posts(create_user, session):
    post_data = [
        {
            "title": "first title",
            "content": "first content",
            "owner_id": create_user['id']
        }, 
        {
            "title": "2nd title",
            "content": "2nd content",
            "owner_id": create_user['id']
        },
        {
            "title": "3rd title",
            "content": "3rd content",
            "owner_id": create_user['id']
        }, 
        {
            "title": "3rd title",
            "content": "3rd content",
            "owner_id": create_user['id']
        }
    ]
    def create_post_model(post):
        return models.Post(**post)

    post_map = map(create_post_model, post_data)
    posts = list(post_map)

    session.add_all(posts)
    session.commit()
    posts = session.query(models.Post).all()
    return posts


@pytest.fixture()
def create_vote(create_posts, create_user, session):
    new_vote = models.Vote(post_id=create_posts[0].id, user_id=create_user["id"])
    session.add(new_vote)
    session.commit()

