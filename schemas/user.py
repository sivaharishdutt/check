from pydantic import BaseModel  #pydantic-Data validation and settings management using Python type hinting.
#The primary means of defining objects in pydantic is via models here it is BaseModel, here User is a model with 4 fields 

class User(BaseModel):#serializer
    
    id:int
    name:str
    email:str
    password:str
 
    

    class Config:              #Pydantic models can be created from arbitrary class instances to support models that map to ORM objects.
        orm_model=True