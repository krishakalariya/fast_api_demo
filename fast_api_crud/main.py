import uvicorn
from fastapi import FastAPI, HTTPException, status, Depends
from sqlalchemy.orm.exc import UnmappedInstanceError

from database import get_db, Base, engine

from schema import Category as SchemaCategory
from schema import Product as SchemaProduct

from models import Category, Product

from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

Base.metadata.create_all(engine)


# to avoid csrftokenError
# app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")


# app.add_middleware(DBSessionMiddleware, db_url=os.environ['DATABASE_URL'])


@app.get("/")
def root():
    """home view"""
    return {"message": "hello world"}


@app.get('/category/')
def get_category(db=Depends(get_db)):
    """get api for category"""
    category = db.query(Category).all()
    return category


@app.get('/product/')
def get_product(db=Depends(get_db)):
    """get api for product"""
    product = db.query(Product).all()
    return product


@app.post('/create/category/', response_model=SchemaCategory)
def post_category(category: SchemaCategory, db=Depends(get_db)):
    """Api for create category"""
    existing_category = db.query(Category).filter(Category.name == category.name).first()
    if existing_category:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Category already exists")
    db_category = Category(name=category.name)
    db.add(db_category)
    db.commit()
    return db_category


@app.post('/create/product/', response_model=SchemaProduct)
def post_product(product: SchemaProduct, db=Depends(get_db)):
    """Api for create product"""
    existing_product = db.query(Product).filter(Product.name == product.name).first()
    exist_category = db.query(Category).filter(Category.id == product.category_id).first()
    if existing_product:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Product already exists.")
    if not exist_category:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Category is not exist.")
    db_product = Product(name=product.name, category_id=product.category_id)
    db.add(db_product)
    db.commit()
    return db_product


@app.delete("/delete/category/{id}")
def delete_category(id: int, db=Depends(get_db)):
    category = db.query(Category).filter(Category.id == id).first()
    if category is None:
        return {"msg": "Category not found"}

    try:
        db.delete(category)
        db.commit()
        return {"msg": "Deleted successfully"}
    except UnmappedInstanceError:
        return {"msg": "Error deleting category"}


@app.delete("/delete/product/{id}")
def delete_product(id: int, db=Depends(get_db)):
    product = db.query(Product).filter(Product.id == id).first()
    if product is None:
        return {"msg": "Product not found"}

    try:
        db.delete(product)
        db.commit()
        return {"msg": "Deleted successfully"}
    except UnmappedInstanceError:
        return {"msg": "Error deleting product"}


@app.put("/update/category/{id}")
def update_category(id: int, new_text: str = "", db=Depends(get_db)):
    category_query = db.query(Category).filter(Category.id == id)
    category = category_query.first()

    if category is None:
        return {"msg": "Category does not exist"}

    try:
        if new_text:
            category.name = new_text
        else:
            return {"msg": "New text is empty"}

        db.add(category)
        db.commit()

        return {"msg": "Category updated successfully"}
    except UnmappedInstanceError:
        return {"msg": "Error updating category"}


@app.put("/update/product/{id}")
def update_product(id: int, new_text: str = "", new_id: int = None, db=Depends(get_db)):
    product_query = db.query(Product).filter(Product.id == id)
    product = product_query.first()

    if product is None:
        return {"msg": "Product does not exist"}

    try:
        if new_text:
            product.name = new_text

        if new_id is not None:
            product.category_id = new_id

        db.add(product)
        db.commit()

        return {"msg": "Product updated successfully"}
    except UnmappedInstanceError:
        return {"msg": "Error updating product"}


@app.get("/menu")
def get_products_by_category(db=Depends(get_db)):
    categories = db.query(Category).all()

    category_products = []

    for category in categories:
        products = db.query(Product).filter(Product.category_id == category.id).all()
        products_data = [{"id": product.id, "name": product.name} for product in products]
        category_products.append({"id": category.id, "category": category.name, "products": products_data})

    return {"data": category_products}


if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        reload=True
    )
