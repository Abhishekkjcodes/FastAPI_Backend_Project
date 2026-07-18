import pytest
import jwt
from jwt.exceptions import InvalidTokenError
from app import schemas
from app.configs import settings

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

def test_root(client):
    res=client.get("/")
    print(res.json().get("message"))
    assert res.json().get("message")=="well this is fast api with bind mounts"
    assert res.status_code ==200
    
def test_create_user(client):
    res=client.post("/users/",json={"email":"heat@hotmail.com","password":"heat123"})
    user_res=schemas.UserResponse(**res.json()) # now this isnt an alternative to the assert statements but pydantic provides us with some validation
    assert res.json().get("email")=="heat@hotmail.com"
    assert res.status_code==201

def test_login_user(test_user,client):
    res=client.post("/login",data={"username":test_user["email"],"password":test_user["password"]})
    # print(res.json())
    body = res.json()
    assert "access_token" in body
    assert body["token_type"] == "bearer"
    payload = jwt.decode(body["access_token"], SECRET_KEY, algorithms=[ALGORITHM])
    uid = payload.get("user_id")
    assert uid is not None
    token_data=schemas.TokenData(id=uid)
    assert token_data.id==test_user["id"]
    assert res.status_code==200

@pytest.mark.parametrize("email,password,status_code",[('wrongemail@gmail.com', 'password123', 401),
('sanjeev@gmail.com', 'wrongpassword', 401),
('wrongemail@gmail.com', 'wrongpassword', 401),
(None, 'password123', 422),
('sanjeev@gmail.com', None, 422)])
def test_incorrect_login(test_user,client,email,password,status_code):
    res=client.post("/login",data={"username":email,"password":password})
    body = res.json()
    assert res.status_code==status_code
    # assert body["detail"]=="Invalid credentials"
    