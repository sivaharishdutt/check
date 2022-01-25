from pydantic import BaseModel
from fastapi import APIRouter,HTTPException,status      #FastAPI is a modern, fast (high-performance), web framework for building APIs in python.
from models.user import User as users
from models.user import Item as items
from models.user import Order as orders
from models.user import OrderItem as orditems
from typing import List
#from sqlalchemy import join
#from sqlalchemy.sql import select
 
from config.db import SessionLocal
user=APIRouter()                    #You want to have the path operations related to your users separated from the rest of the code, to keep it organized,You can create the path operations for that module using APIRouter.

session=SessionLocal()

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
    
    user_to_update.name=user.name
    user_to_update.email=user.email
    user_to_update.password=user.password
 
     
    
    
    session.commit()

    return user_to_update


@user.put('/item/{id}',response_model=Item,status_code=status.HTTP_200_OK)
def update_a_item(id:int,item:Item):
    item_to_update=session.query(itemTable).filter(itemTable.id==id).first()
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

@user.post('/id-of-users-who-made-orders/',response_model=Order,status_code=status.HTTP_201_CREATED)
def add_user_order(ord_id:Order):
    new_order=orderTable(
        user_id=ord_id.user_id
    ) 
    session.add(new_order)
    session.commit()

    return new_order 

@user.get('/total-orders-made/',response_model=List[Order],status_code=200)
def fetch_all_orders():
    all_orders=session.query(orderTable).all()

    return all_orders

@user.post('/items-that-are-bought-with-a-particular-order/',response_model=OrderItem,status_code=status.HTTP_201_CREATED)
def add_user_order(orderItem_id:OrderItem):
    order_items=orderItemTable(
        order_id=orderItem_id.order_id,
        item_id=orderItem_id.item_id,
    ) 
    session.add(order_items)
    session.commit()

    return order_items 

@user.get('/items-that-are-bought-wiht-single-order-id/{id}' )
def items_wrt_a_order(id:int):
    OrderItems = session.query(orderTable.user_id.label('user id:'),orderItemTable.item_id.label('product id:'),itemTable.name.label('product name:'),itemTable.max_discounted_price.label('product discounted price:')).join(orderItemTable,orderTable.id==orderItemTable.order_id,isouter=True).join(itemTable,orderItemTable.item_id==itemTable.id).filter(orderTable.id==id).all()
    
    if OrderItems is None:
        raise HTTPException(status_code=404,detail="that particular order id does not exist")
     
    return OrderItems

@user.get('/name-of-user-along-with-items-bought-wrt-order-id/{id}' )
def name_of_user_wrt_ordID(id:int):
    user_names_with_items = session.query(userTable.name.label('user name'),itemTable.name.label('product name'),itemTable.max_discounted_price.label('product price')).join(orderTable,userTable.id==orderTable.user_id,isouter=True).join(orderItemTable,orderTable.id==orderItemTable.order_id,isouter=True).join(itemTable,orderItemTable.item_id==itemTable.id,isouter=True).filter(orderTable.id==id).all()
    
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