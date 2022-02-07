from pydantic import BaseModel
from fastapi import APIRouter,HTTPException,status,Depends    #FastAPI is a modern, fast (high-performance), web framework for building APIs in python.
from models.user import User as users
from models.user import Item as items
from models.user import Order as orders
from models.user import OrderItem as orditems
from typing import List
#from sqlalchemy import join
#from sqlalchemy.sql import select
 
from config.db import SessionLocal
from sqlalchemy.orm import Session
user=APIRouter()                    #You want to have the path operations related to your users separated from the rest of the code, to keep it organized,You can create the path operations for that module using APIRouter.

#session=SessionLocal()

class User(BaseModel):
    id:int
    #item_id:int
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


class Order(BaseModel):
    id:int
    user_id:int

    class Config:
        orm_mode=True

class OrderItem(BaseModel):
    id:int
    order_id:int
    item_id:int

    class Config:
        orm_mode=True

userTable=users
itemTable=items
orderTable=orders
orderItemTable=orditems

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()
 

@user.get('/users/',response_model=List[User],status_code=200)
def fetch_all_users(db:Session=Depends(get_db)):
    all_users=db.query(userTable).all()

    return all_users

@user.get('/items/',response_model=List[Item],status_code=200)
def fetch_all_items(db:Session=Depends(get_db)):
    all_items=db.query(itemTable).all()

    return all_items

@user.get('/users/{id}',response_model=User,status_code=status.HTTP_200_OK)
def fetch_user(id:int,db:Session=Depends(get_db)):
    single_user=db.query(userTable).filter(userTable.id==id).first()
    
    if single_user is None:
        raise HTTPException(status_code=404,detail="User does not exist")
    
    return single_user

@user.get('/items/{id}',response_model=Item,status_code=status.HTTP_200_OK)
def fetch_item(id:int,db:Session=Depends(get_db)):
    item_data=db.query(itemTable).filter(itemTable.id==id).first()
    
    if item_data is None:
        raise HTTPException(status_code=404,detail="Item does not exist")
    
    return item_data

@user.post('/users/',response_model=User,status_code=status.HTTP_201_CREATED)
def create_a_user(user_id:User, db:Session=Depends(get_db) ):
    db_user=db.query(userTable).filter(userTable.name==user_id.name).first()

    if db_user is not None:
        raise HTTPException(status_code=400,detail="User Already Exists")

    new_user=userTable(
        name=user_id.name,
        email=user_id.email,
        password=user_id.password
    ) 

     
    db.add(new_user)
    db.commit()

    return new_user 


@user.post('/items/',response_model=Item,status_code=status.HTTP_201_CREATED)
def create_an_item(itemID:Item,db:Session=Depends(get_db) ):
    db_item=db.query(itemTable).filter(itemTable.name==itemID.name).first()

    if db_item is not None:
        raise HTTPException(status_code=400,detail="Item Already Exists")

    new_Item=itemTable(
       
       
        name=itemID.name,
        price=itemID.price,
        max_discounted_price=itemID.max_discounted_price
        
    ) 

     
    db.add(new_Item)
    db.commit()

    return new_Item 


@user.put('/users/{id}',response_model=User,status_code=status.HTTP_200_OK)
def update_a_user(id:int,user:User,db:Session=Depends(get_db)):
    user_to_update=db.query(userTable).filter(userTable.id==id).first()
    
    user_to_update.name=user.name
    user_to_update.email=user.email
    user_to_update.password=user.password
 
     
    
    
    db.commit()

    return user_to_update


@user.put('/items/{id}',response_model=Item,status_code=status.HTTP_200_OK)
def update_a_item(id:int,item:Item,db:Session=Depends(get_db)):
    item_to_update=db.query(itemTable).filter(itemTable.id==id).first()
    item_to_update.name=item.name
    item_to_update.price=item.price
    item_to_update.max_discounted_price=item.max_discounted_price




    db.commit()

    return item_to_update

@user.delete('/users/{id}')
def delete_user(id:int,db:Session=Depends(get_db)):
    user_to_delete=db.query(userTable).filter(userTable.id==id).first()

    if user_to_delete is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="resource not found")

    db.delete(user_to_delete)
    db.commit()


    return user_to_delete

@user.delete('/items/{id}')
def delete_item(id:int,db:Session=Depends(get_db)):
    item_to_delete=db.query(itemTable).filter(itemTable.id==id).first()

    if item_to_delete is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="item not found")

    db.delete(item_to_delete)
    db.commit()


    return item_to_delete

@user.post('/orders',response_model=Order,status_code=status.HTTP_201_CREATED)
def add_user_order(ord_id:Order,db:Session=Depends(get_db)):
    new_order=orderTable(
        user_id=ord_id.user_id
    ) 
    db.add(new_order)
    db.commit()

    return new_order 

@user.get('/users/orders',response_model=List[Order],status_code=200)
def fetch_all_orders(db:Session=Depends(get_db)):
    all_orders=db.query(orderTable).all()

    return all_orders

@user.post('/users/{user-id}/orders',response_model=OrderItem,status_code=status.HTTP_201_CREATED)
def add_user_order(orderItem_id:OrderItem,db:Session=Depends(get_db)):
    order_items=orderItemTable(
        order_id=orderItem_id.order_id,
        item_id=orderItem_id.item_id,
    ) 
    db.add(order_items)
    db.commit()

    return order_items 

@user.get('/orders/{id}/items' )
def items_wrt_a_order(id:int,db:Session=Depends(get_db)):
    OrderItems = db.query(orderTable.user_id.label('user id:'),orderItemTable.item_id.label('product id:'),itemTable.name.label('product name:'),itemTable.max_discounted_price.label('product discounted price:')).join(orderItemTable,orderTable.id==orderItemTable.order_id,isouter=True).join(itemTable,orderItemTable.item_id==itemTable.id).filter(orderTable.id==id).all()
    
    if OrderItems is None:
        raise HTTPException(status_code=404,detail="that particular order id does not exist")
     
    return OrderItems

@user.get('/users/orders/{id}/items/item-detials' )
def name_of_user_wrt_ordID(id:int,db:Session=Depends(get_db)):
    user_names_with_items = db.query(userTable.name.label('user name'),itemTable.name.label('product name'),itemTable.max_discounted_price.label('product price')).join(orderTable,userTable.id==orderTable.user_id,isouter=True).join(orderItemTable,orderTable.id==orderItemTable.order_id,isouter=True).join(itemTable,orderItemTable.item_id==itemTable.id,isouter=True).filter(orderTable.id==id).all()
    
    if user_names_with_items is None:
        raise HTTPException(status_code=404,detail="that particular order id does not exist")
     
    return user_names_with_items


"""
@user.get('/giving-details-of-users/')
def fetch_all_users_data_along_with_items():
    results=session.query(userTable,itemTable).join(userTable).all()
    return results

@user.get('/giving-user-details/' )
def fetch_user_details_with_items():
    singleUserItem = session.query(userTable,itemTable).join(itemTable,userTable.item_id==itemTable.id,isouter=True).all()
    print(singleUserItem)
    if singleUserItem is None:
        raise HTTPException(status_code=404,detail="that particular id does not exist")
     
    return singleUserItem

@user.get('/giving-item-details/' )
def fetch_item_details_with_users():
    Item = session.query(itemTable,userTable).join(userTable,userTable.item_id==itemTable.id,isouter=True).all()
    print(Item)
    if Item is None:
        raise HTTPException(status_code=404,detail="that particular id does not exist")
     
    return Item

"""

""""

@user.get('/join/{id}')
def which_user_bought_what_item(id:int):
    j=userTable.join(itemTable,userTable.c.item_id==itemTable.c.id)
    stmt=select([userTable]).select_from(j)
    answer=session.query(stmt)

    return answer

@user.get('/join/{id}')
def check_user_names_items_who_bought_ge_100():
    for c,i in session.query(userTable,itemTable).filter(userTable.item_id==itemTable.id and itemTable.max_discounted_price>=100):
        print ("ID: {} Name: {} Item Name: {} Amount: {}".format(c.id,c.name, i.name, i.max_discounted_price))

    return {}


"""