from sqlalchemy import Column #sqlAlchemy is a sqltoolkit and object relational mapper ORM,orm- a programming technique for converting data between incompatible type systems using object-oriented programming languages.
from sqlalchemy import MetaData
from config.db import engine
from sqlalchemy.sql.sqltypes import Integer,String
from sqlalchemy.ext.declarative import declarative_base

Base=declarative_base()

meta=MetaData()

class User(Base):
    __tablename__='users'
    id=Column(Integer,primary_key=True)
    name=Column(String(255))
    email=Column(String(255))
    password=Column(String(255))
    
    


    

Base.metadata.create_all(engine)