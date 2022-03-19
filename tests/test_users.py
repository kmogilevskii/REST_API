from app.schemas import UserReturn
from .database import client, session

def test_root(client):
    res = client.get("/")
    print(res.json())
    print(res.status_code)

def test_create_user(client):
    res = client.post("/users/", json={"email": "konstest@gmail.com", "password": "password123"})
    new_user = UserReturn(**res.json())
    assert new_user.email == "konstest@gmail.com"
    assert res.status_code == 201

def test_login_user(client):
    res = client.post("/login", data={"username": "konstest@gmail.com", "password": "password123"})
    assert res.status_code == 200