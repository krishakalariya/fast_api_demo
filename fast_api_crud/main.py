from fastapi import FastAPI
from fastapi_sqlalchemy import DBSessionMiddleware, db
from sqlalchemy.orm.exc import UnmappedInstanceError

from schema import Category as SchemaCategory
from schema import Product as SchemaProduct

from models import Category, Product

import os
from dotenv import load_dotenv

load_dotenv('.env')

app = FastAPI()

# to avoid csrftokenError
app.add_middleware(DBSessionMiddleware, db_url=os.environ['DATABASE_URL'])


@app.get("/")
async def root():
    return {"message": "hello world"}


@app.get('/category/')
async def get_category():
    category = db.session.query(Category).all()
    return category


@app.get('/product/')
async def get_product():
    product = db.session.query(Product).all()
    return product


@app.post('/create/category/', response_model=SchemaCategory)
async def post_category(category: SchemaCategory):
    db_author = Category(name=category.name)
    db.session.add(db_author)
    db.session.commit()
    return db_author


@app.post('/create/product/', response_model=SchemaProduct)
async def post_product(product: SchemaProduct):
    db_author = Product(name=product.name, category_id=product.category_id)
    db.session.add(db_author)
    db.session.commit()
    return db_author


@app.delete("/delete/category/{id}")
async def delete_category(id: int):
    category = db.session.query(Category).filter(Category.id == id).first()
    if category is None:
        return {"msg": "Category not found"}

    try:
        db.session.delete(category)
        db.session.commit()
        return {"msg": "Deleted successfully"}
    except UnmappedInstanceError:
        return {"msg": "Error deleting category"}


@app.delete("/delete/product/{id}")
async def delete_product(id: int):
    product = db.session.query(Product).filter(Product.id == id).first()
    if product is None:
        return {"msg": "Product not found"}

    try:
        db.session.delete(product)
        db.session.commit()
        return {"msg": "Deleted successfully"}
    except UnmappedInstanceError:
        return {"msg": "Error deleting product"}


@app.put("/update/category/{id}")
async def update_category(id: int, new_text: str = "", is_complete: bool = False):
    category_query = db.session.query(Category).filter(Category.id == id)
    category = category_query.first()

    if category is None:
        return {"msg": "Category does not exist"}

    try:
        if new_text:
            category.name = new_text
        else:
            return {"msg": "New text is empty"}

        db.session.add(category)
        db.session.commit()

        return {"msg": "Category updated successfully"}
    except UnmappedInstanceError:
        return {"msg": "Error updating category"}


@app.put("/update/product/{id}")
async def update_product(id: int, new_text: str = "", new_id: int = None, is_complete: bool = False):
    product_query = db.session.query(Product).filter(Product.id == id)
    product = product_query.first()

    if product is None:
        return {"msg": "Product does not exist"}

    try:
        if new_text:
            product.name = new_text

        if new_id is not None:
            product.category_id = new_id

        db.session.add(product)
        db.session.commit()

        return {"msg": "Product updated successfully"}
    except UnmappedInstanceError:
        return {"msg": "Error updating product"}


@app.get("/menu")
async def get_products_by_category():
    categories = db.session.query(Category).all()

    category_products = []

    for category in categories:
        products = db.session.query(Product).filter(Product.category_id == category.id).all()
        products_data = [{"id": product.id, "name": product.name} for product in products]
        category_products.append({"id": category.id, "category": category.name, "products": products_data})

    return {"data": category_products}
