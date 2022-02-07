import unittest
from h11 import CLIENT

from sqlalchemy import false, true
from fastapi.testclient import TestClient
 
 
from index import app

  
client= TestClient(app)
class TestUsers(unittest.TestCase):
    
    def test_fetch_user_1(self):
            response=client.get("/users/1")
            assert response.status_code==200
            assert response.json()== {
                                        "id":1,
                                        "name": "sivaUpdated",
                                        "email": "siva@gamil.com",
                                        "password": "sivaUpdatedPWD"
                                    }
                            
    def test_fetch_user_2(self):
        response=client.get("/users/2")
        assert response.status_code==200
        assert response.json()=={
                                    "id": 2,
                                    "name": "harish",
                                    "email": "harish@gamil.com",
                                    "password": "harish_password"
                                }
    def test_fetch_user_3(self):
        response=client.get("/users/3")
        
        assert response.status_code==200
        assert response.json()=={
                                    "id": 3,
                                    "name": "dutt",
                                    "email": "dutt@gamil.com",
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
"""    
    def test_create_user(self):
        response=client.post("/users/",json={
                                                "id": 1234542,
                                                "name": "test14",
                                                "email": "test14@gmail.com",
                                                "password": "test14_pwd"
                                            }
                            )
        assert response.status_code == 200, response.text
        data=response.json()
         
        user_id=data["id"]

        response=client.get("/users/{user_id}")
        assert response.status_code==200, response.text
        assert response.json()=={
                                    "id":{user_id},
                                    "name": "test{user_id}",
                                    "email": "test{user_id}@gmail.com",
                                    "password": "test{user_id}_pwd"
                                }
"""     
    


    

     
