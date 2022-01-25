from typing import List
from pydantic import Json
from sqlalchemy import Column, ForeignKey #sqlAlchemy is a sqltoolkit and object relational mapper ORM,orm- a programming technique for converting data between incompatible type systems using object-oriented programming languages.
from sqlalchemy import MetaData
from config.db import engine
from sqlalchemy.sql.sqltypes import Integer,String
from sqlalchemy.ext.declarative import declarative_base

Base=declarative_base()

meta=MetaData()

class User(Base):
    __tablename__='users'
    id=Column(Integer,primary_key=True)
    item_id=Column(Integer,ForeignKey("items.id"))
    name=Column(String(255))
    email=Column(String(255))
    password=Column(String(255))
     
class Item(Base):
    __tablename__='items'
    id=Column(Integer,primary_key=True)
    name=Column(String(255))
    price=Column(Integer)
    max_discounted_price=Column(Integer)

Base.metadata.create_all(engine)

"""

Order:
ord id:pk
ordid: 1 
user id:fk
user id:
//items_list:Json

orderItem:
order id:fk
item id:fk


user=siva
amazon 3 prods
i1: 
i2:
i3:


lolcalhost/users/6/items/89/prices?limit=100&variable=20

@user.get('/users/{ex1}/items/{ex2}/prices/')
def check(ex1:int,ex2:int,limit:int=100,variable:int=20):
    pass


user:
id pk,
name,
email,
pwd.

item:
id pk,
name,
price,
max_discounted_price.

order:
id pk,
user-id fk,
item-id fk.

relationships:
user-order m:1 coz one user can make many orders
order-item 1:n coz one order can have many items

overall it becomes many-many relations


"""