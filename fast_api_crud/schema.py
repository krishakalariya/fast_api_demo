# build a schema using pydantic
from pydantic import BaseModel


class Category(BaseModel):
    name: str

    class Config:
        orm_mode = True


class Product(BaseModel):
    name: str
    category_id: int
