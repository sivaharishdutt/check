from pydantic import BaseModel

from fastapi import APIRouter,HTTPException,status      #FastAPI is a modern, fast (high-performance), web framework for building APIs in python.
from models.user import User as users
from models.user import Item as items
from typing import List
 
 
from config.db import SessionLocal
user=APIRouter()                    #You want to have the path operations related to your users separated from the rest of the code, to keep it organized,You can create the path operations for that module using APIRouter.

session=SessionLocal()

class User(BaseModel):
    id:int
    item_id:int
    name:str
    email:str
    password:str
    


    class Config:                   ##Pydantic models can be created from arbitrary class instances to support models that map to ORM objects.
        orm_mode=True 

class Item(BaseModel):
    id:int
    name:str
    price:int
    max_discounted_price:int



    class Config:
        orm_mode=True


 

userTable=users
itemTable=items


 

@user.get('/user/',response_model=List[User],status_code=200)
def fetch_all_users():
    all_users=session.query(userTable).all()

    return all_users
@user.get('/item/',response_model=List[Item],status_code=200)
def fetch_all_items():
    all_items=session.query(itemTable).all()

    return all_items

@user.get('/user/{id}',response_model=User,status_code=status.HTTP_200_OK)
def fetch_user(id:int):
    single_user=session.query(userTable).filter(userTable.id==id).first()
    
    if single_user is None:
        raise HTTPException(status_code=404,detail="User does not exist")
    
    return single_user

@user.get('/item/{id}',response_model=Item,status_code=status.HTTP_200_OK)
def fetch_item(id:int):
    item_data=session.query(itemTable).filter(itemTable.id==id).first()
    
    if item_data is None:
        raise HTTPException(status_code=404,detail="Item does not exist")
    
    return item_data

@user.post('/user/',response_model=User,status_code=status.HTTP_201_CREATED)
def create_a_user(user_id:User ):
    db_user=session.query(userTable).filter(userTable.name==user_id.name).first()

    if db_user is not None:
        raise HTTPException(status_code=400,detail="User Already Exists")

    new_user=userTable(
        item_id=user_id.item_id,
        name=user_id.name,
        email=user_id.email,
        password=user_id.password
    ) 

     
    session.add(new_user)
    session.commit()

    return new_user 


@user.post('/item/',response_model=Item,status_code=status.HTTP_201_CREATED)
def create_an_item(itemID:Item ):
    db_item=session.query(itemTable).filter(itemTable.name==itemID.name).first()

    if db_item is not None:
        raise HTTPException(status_code=400,detail="Item Already Exists")

    new_Item=itemTable(
       
        id=itemID.id,
        name=itemID.name,
        price=itemID.price,
        max_discounted_price=itemID.max_discounted_price
        
    ) 

     
    session.add(new_Item)
    session.commit()

    return new_Item 


@user.put('/user/{id}',response_model=User,status_code=status.HTTP_200_OK)
def update_a_user(id:int,user:User):
    user_to_update=session.query(userTable).filter(userTable.id==id).first()
    user_to_update.item_id=user.item_id
    user_to_update.name=user.name
    user_to_update.email=user.email
    user_to_update.password=user.password
 
     
    
    
    session.commit()

    return user_to_update


@user.put('/item/{id}',response_model=Item,status_code=status.HTTP_200_OK)
def update_a_item(id:int,item:Item):
    item_to_update=session.query(itemTable).filter(itemTable.id==item.id).first()
    item_to_update.id=item.id
    item_to_update.name=item.name
    item_to_update.price=item.price
    item_to_update.max_discounted_price=item.max_discounted_price




    session.commit()

    return item_to_update

@user.delete('/user/{id}')
def delete_user(id:int):
    user_to_delete=session.query(userTable).filter(userTable.id==id).first()

    if user_to_delete is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="resource not found")

    session.delete(user_to_delete)
    session.commit()


    return user_to_delete

@user.delete('/item/{id}')
def delete_item(id:int):
    item_to_delete=session.query(itemTable).filter(itemTable.id==id).first()

    if item_to_delete is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="item not found")

    session.delete(item_to_delete)
    session.commit()


    return item_to_delete

results=session.query(userTable,itemTable).join(userTable).all()

@user.get('/join/')
def fetch_all_users_data_along_with_items():
    
    return results

@user.get('/join/{id}' )
def fetch_single_user_item_details(id:int):
    singleUserItem = session.query(userTable, itemTable).join(userTable).filter(userTable.id==id).all()
    if singleUserItem is None:
        raise HTTPException(status_code=404,detail="that particular id does not exist")
     
    return singleUserItem