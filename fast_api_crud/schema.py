#build a schema using pydantic
from pydantic import BaseModel

class Category(BaseModel):
    name : str

class Product(BaseModel):
    name: str
    category_id :int

# class Book(BaseModel):
#     title: str
#     rating: int
#     author_id: int
#
#     class Config:
#         orm_mode = True
#
# class Author(BaseModel):
#     name:str
#     age:int
#
#     class Config:
#         orm_mode = True