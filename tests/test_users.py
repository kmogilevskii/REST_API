import pytest
from app import schemas
from app.config import settings
from jose import jwt


def test_login_user(client, create_user):
    data = {
        "username": create_user["email"],
        "password": create_user["password"]
    }
    res = client.post("/login", data=data)
    login_res = schemas.Token(**res.json())
    payload = jwt.decode(login_res.access_token, settings.secret_key, algorithms=[settings.algorithm])
    id = payload.get("user_id")
    assert id == create_user["id"]
    assert login_res.token_type == "bearer"
    assert res.status_code == 200

@pytest.mark.parametrize("email, password, status_code", [
    ('wrongemail@gmail.com', 'password123', 403),
    ('sanjeev@gmail.com', 'wrongpassword', 403),
    ('wrongemail@gmail.com', 'wrongpassword', 403),
    (None, 'password123', 422),
    ('sanjeev@gmail.com', None, 422)
])
def test_failed_login(client, email, password, status_code):
    res = client.post("/login", data={
        "username": email,
        "password": password
    })
    assert res.status_code == status_code
    # assert res.json()["detail"] == "Invalid credentials."
    