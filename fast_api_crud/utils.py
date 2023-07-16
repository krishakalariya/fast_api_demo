from sqlalchemy.orm import Session

from models import Category
from schema import Category as SchemaCategory

class ItemRepo:

    async def create(db: Session, item: SchemaCategory):
        db_item = Category(name=item.name)
        db.add(db_item)
        db.commit()
        db.refresh(db_item)
        return db_item

    def fetch_by_id(db: Session, _id):
        return db.query(Category).filter(Category.id == _id).first()