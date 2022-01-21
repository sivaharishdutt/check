from pydantic import BaseModel
 
from fastapi import APIRouter,HTTPException,status      #FastAPI is a modern, fast (high-performance), web framework for building APIs in python.
from models.user import User as users
from typing import List
 
from config.db import SessionLocal
user=APIRouter()                    #You want to have the path operations related to your users separated from the rest of the code, to keep it organized,You can create the path operations for that module using APIRouter.

session=SessionLocal()

class User(BaseModel):
    id:int
    name:str
    email:str
    password:str
    
   
    
    class Config:                   ##Pydantic models can be created from arbitrary class instances to support models that map to ORM objects.
        orm_mode=True 

userTable=users

@user.get('/',response_model=List[User],status_code=200)
def fetch_users():
    all_users=session.query(userTable).all()

    return all_users

@user.get('/{id}',response_model=User,status_code=status.HTTP_200_OK)
def fetch_user(id:int):
    single_user=session.query(userTable).filter(userTable.id==id).first()
    
    if single_user is None:
        raise HTTPException(status_code=404,detail="User does not exist")
    
    return single_user

@user.post('/',response_model=User,status_code=status.HTTP_201_CREATED)
def create_a_user(user_id:User):
    #db_user=session.query(userTable).filter(userTable.name==user_id.name).first()

    #if db_user is not None:
    #    raise HTTPException(status_code=400,detail="User Already Exists")

    new_user=userTable(
    name=user_id.name,
    email=user_id.email,
    password=user_id.password,
     
    
    
    )
    

    session.add(new_user)
    session.commit()

    return new_user


@user.put('/{id}',response_model=User,status_code=status.HTTP_200_OK)
def update_a_user(id:int,user:User):
    user_to_update=session.query(userTable).filter(userTable.id==id).first()
    user_to_update.name=user.name
    user_to_update.email=user.email
    user_to_update.password=user.password
 
     
    

    session.commit()

    return user_to_update

@user.delete('/{id}')
def delete_user(id:int):
    user_to_delete=session.query(userTable).filter(userTable.id==id).first()

    if user_to_delete is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="resource not found")

    session.delete(user_to_delete)
    session.commit()


    return user_to_delete






