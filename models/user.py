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
    #item_id=Column(Integer,ForeignKey("items.id"))
    name=Column(String(255))
    email=Column(String(255))
    password=Column(String(255))
     
class Item(Base):
    __tablename__='items'
    id=Column(Integer,primary_key=True)
    name=Column(String(255))
    price=Column(Integer)
    max_discounted_price=Column(Integer)

class Order(Base):
    __tablename__='orders'
    id=Column(Integer,primary_key=True)
    user_id=Column(Integer,ForeignKey("users.id"))

class OrderItem(Base):
    __tablename__='order_items'
    id=Column(Integer,primary_key=True)
    order_id=Column(Integer,ForeignKey("orders.id"))
    item_id=Column(Integer,ForeignKey("items.id"))

Base.metadata.create_all(engine)

"""

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

orderItem:
id pk
ord_id:fk
item_id:fk

relationships:
user-order m:1 coz one user can make many orders
order-item 1:n coz one order can have many items

overall it becomes many-many relations


"""