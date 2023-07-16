from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

Base = declarative_base()


class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)


class Product(Base):
    __tablename__ ="products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    category_id = Column(Integer, ForeignKey('categories.id'))



# class Book(Base):
#     __tablename__ = 'book'
#     id  = Column(Integer, primary_key=True, index=True)
#     title = Column(String)
#     rating = Column(Float)
#     time_created = Column(DateTime(timezone=True), server_default=func.now())
#     time_updated = Column(DateTime(timezone=True), onupdate=func.now())
#     author_id = Column(Integer, ForeignKey('author.id'))
#
#     author = relationship('Author')
#
#
# class Author(Base):
#     __tablename__ = 'author'
#     id = Column(Integer, primary_key=True)
#     name = Column(String)
#     age = Column(Integer)
#     time_created = Column(DateTime(timezone=True), server_default=func.now())
#     time_updated = Column(DateTime(timezone=True), onupdate=func.now())
