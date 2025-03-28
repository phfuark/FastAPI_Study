from typing import List
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session



from fastapi import Depends, FastAPI, HTTPException

from models import *

app = FastAPI()

DATABASE_URL = 'sqlite:///./database.db'

# Criação da engine do SQLAlchemy =================================================================
engine = create_engine(DATABASE_URL, connect_args={'check_same_thread': False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    price = Column(Float, index=True)
    description = Column(String, index=True)

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

 # URLS ===========================================================================================

@app.get('/get_product/', response_model=List[ProductResponse])
def read_product(skip: int = 0, limit = 10, db: Session = Depends(get_db)):
    products = db.query(Product).offset(skip).limit(limit).all()
    return products

@app.get('/get_product/{product_id}', response_model=List[ProductResponse])
def read_products(user_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == user_id).first()

    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@app.post('/create_product/', response_model=ProductResponse)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    db_product = Product(name=product.name, description=product.description, price=product.price)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

@app.put('/put_product/{product_id}', response_model=ProductResponse)
def update_product(product_id: int, product: ProductUpdate, db: Session = Depends(get_db)):
    db_product = Product(name=product.name, description=product.description, price=product.price)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    db_product.name = product.name if product.name is not None else db_product.name
    db_product.description = product.description if product.description is not None else db_product.description
    db_product.price = product.price if product.price is not None else db_product.price
    db.commit()
    db.refresh(db_product)
    return db_product
