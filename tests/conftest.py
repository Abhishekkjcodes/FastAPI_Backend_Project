from fastapi.testclient import TestClient
import pytest
from app.database import get_db
from app.main import app
from app import models
from app.Oauth2 import create_access_token
from sqlalchemy import create_engine,select
from sqlalchemy.orm import sessionmaker
from app.configs import TestSettings
from app import models

testSettings = TestSettings()

engine = create_engine(f"postgresql+psycopg://{testSettings.testing_username}:{testSettings.testing_password}@{testSettings.testing_hostname}:{testSettings.testing_port}/{testSettings.testing_name}")
TestingSessionLocal=sessionmaker(engine)

@pytest.fixture()
def session():
    #this can be done using alembic as well
    models.Base.metadata.drop_all(bind=engine)
    models.Base.metadata.create_all(bind=engine)
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
    yield TestClient(app)

@pytest.fixture
def test_user(client):
    res=client.post("/users/",json={"email":"abhi@example.com","password":"password123"})
    assert res.json().get("email")=="abhi@example.com"
    assert res.status_code==201
    data=res.json()
    data["password"]="password123"
    return data

@pytest.fixture
def test_user2(client):
    res=client.post("/users/",json={"email":"test@example.com","password":"password123"})
    assert res.json().get("email")=="test@example.com"
    assert res.status_code==201
    data=res.json()
    data["password"]="password123"
    return data

@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": test_user['id']})

@pytest.fixture
def authorized_client(client,token):
    client.headers={
    **client.headers,
    "Authorization": f"Bearer {token}"
    }
    return client

@pytest.fixture
def test_posts(test_user,test_user2,session):
    posts_data=[
        models.Post(title="first title", content="first content", user_id=test_user['id']),
        models.Post(title="2nd title", content="2nd content", user_id=test_user['id']),
        models.Post(title="3rd title", content="3rd content", user_id=test_user['id']),
        models.Post(title="4th title", content="4th content", user_id=test_user2['id'])
    ]
    # u can use a map as well
    session.add_all(posts_data)
    session.commit()
    posts = session.scalars(select(models.Post)).all()
    return posts
