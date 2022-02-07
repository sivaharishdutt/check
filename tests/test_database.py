  # test_database.py
import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from index import app
from routes.user import get_db
from fastapi.testclient import TestClient
from models.user import Base


SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:root@localhost:3306/testCaseDB"

 

engine_test = create_engine(SQLALCHEMY_DATABASE_URL)
print("connecting testing database")

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine_test)

Base.metadata.create_all(bind=engine_test)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

print("testing started")
client= TestClient(app)
class TestUsers(unittest.TestCase):
    
    def test_fetch_user_1(self):
            response=client.get("/users/1")
            assert response.status_code==200
            assert response.json()== {
                                        "id":1,
                                        "name": "test_check99",
                                        "email": "CHECK1@gmail.com",
                                        "password": "chimichangas4life"
                                    }
                            
    def test_fetch_user_2(self):
        response=client.get("/users/2")
        assert response.status_code==200
        assert response.json()=={
                                    "id":2,
                                    "name": "sivaUpdated",
                                    "email": "siva@gmail.com",
                                    "password": "sivaUpdatedPWD"
                                }
    def test_fetch_user_3(self):
        response=client.get("/users/3")
        
        assert response.status_code==200
        assert response.json()=={
                                    "id": 3,
                                    "name": "dutt",
                                    "email": "dutt@gmail.com",
                                    "password": "dutt_password"
                                }
                          
    def test_item_1(self):
        response=client.get("/items/1")
        assert response.status_code==200
        assert response.json()=={
                                    "id": 1,
                                    "name": "pen_with_box",
                                    "price": 200,
                                    "max_discounted_price": 180
                                }
    
    def test_item_2(self):
        response=client.get("/items/2")
        assert response.status_code==200
        assert response.json()=={
                                    "id": 2,
                                    "name": "pencil",
                                    "price": 10,
                                    "max_discounted_price": 8
                                }
    
    def test_create_a_user(self):
        response = client.post(
            "/users/",
            json={"id":1,"name":"test_check99","email": "CHECK1@gmail.com", "password": "chimichangas4life"},
        )
        assert response.status_code == 200, response.text
        data = response.json()
        assert "id" in data
        user_id = data["id"]

        response = client.get("/users/{user_id}")
        assert response.status_code == 200, response.text
        data = response.json()
        assert data["name"] == "test_check99"
        assert data["email"] == "deadpool@example.com"
        assert data["password"] == "chimichangas4life"


print("testing ended")