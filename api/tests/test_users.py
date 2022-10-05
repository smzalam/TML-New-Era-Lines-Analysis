import pytest
from jose import jwt
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from .. import database
from .. import schemas
from .. import confidential

def test_create_user(client):
    res = client.post(
        "/users/", json={"email": "hello123@gmail.com", "password": "password123"})
    print(res.json)
    new_user = schemas.UserOut(**res.json())
    print(new_user)
    assert new_user.email == "hello123@gmail.com"
    assert res.status_code == 201


# def test_login_user(test_user, client):
#     res = client.post(
#         "/login", data={"username": test_user['email'], "passwosrd": test_user['password']})
#     login_res = schemas.Token(**res.json())
#     payload = jwt.decode(login_res.access_token,
#                          settings.secret_key, algorithms=[settings.algorithm])
#     id = payload.get("user_id")
#     assert id == test_user['id']
#     assert login_res.token_type == "bearer"
#     assert res.status_code == 200


# @pytest.mark.parametrize("email, password, status_code", [
#     ('wrongemail@gmail.com', 'password123', 403),
#     ('h@gmail.com', 'wrongpassword', 403),
#     ('wrongemail@gmail.com', 'wrongpassword', 403),
#     (None, 'password123', 422),
#     ('h@gmail.com', None, 422)
# ])
# def test_incorrect_login(test_user, client, email, password, status_code):
#     res = client.post(
#         "/login", data={"username": email, "password": password})

#     assert res.status_code == status_code

