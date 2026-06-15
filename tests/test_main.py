import pytest
from jose import jwt
from app.userHandler import check_User
from app.authHandler import KEY,ALG,MIN

def test_check_env_var():
    print(MIN)
    assert isinstance(MIN, int)

def test_user_login():

    test_token = check_User('Dr.Strange','TheMultiverse')

    assert len(test_token) > 0
    assert isinstance(test_token, str)

    check_payload = jwt.decode(test_token,KEY,algorithms=ALG)

    assert check_payload["sub"] == "9"
    assert check_payload["role"] == "admin"