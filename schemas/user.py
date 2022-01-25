from pydantic import BaseModel  #pydantic-Data validation and settings management using Python type hinting.
#The primary means of defining objects in pydantic is via models here it is BaseModel, here User is a model with 4 fields 

class User(BaseModel):#serializer
    
    user_id:int
    user_name:str
    user_email:str
    item_id:int
    user_password:str
 
    

    class Config:              #Pydantic models can be created from arbitrary class instances to support models that map to ORM objects.
        orm_model=True

class Item(BaseModel):
    item_id:int
    item_name:str
    item_price:int
    item_max_discounted_price:int

    class Config:
        orm_mode=True
