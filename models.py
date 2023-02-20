from enum import unique
from peewee import *
import os

products_db = SqliteDatabase(os.path.join(os.getcwd(), os.path.basename("Products.db")))
products_db.connect()



class BaseModel(Model):
    
    class Meta:
        database = products_db

    

class User(BaseModel):
    name = CharField(unique=True)
    password = CharField()

class Product(BaseModel):
    name = CharField(index=True)
    description = TextField()
    pack = CharField()
    











