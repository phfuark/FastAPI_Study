from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()

from sqlalchemy import create_engine

DATABASE_URL = 'sqlite:///./database.db'
engine = create_engine(DATABASE_URL, connect_args={'check_same_thread': False})

product_supplier = Table(
    'product_supplier', Base.metadata,
    Column('product_id', Integer, ForeignKey('products.id')),
    Column('supplier_id', Integer, ForeignKey('suppliers.id'))
)


sale_product = Table(
    'sale_product', Base.metadata,
    Column('sale_id', Integer, ForeignKey('sales.id')),
    Column('product_id', Integer, ForeignKey('products.id')),
    Column('quantity', Integer)
)


class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    price = Column(Float)
    quantity = Column(Integer)  
    
    
    suppliers = relationship("Supplier", secondary=product_supplier, back_populates="products")
    
    
    cards = relationship("CardProduct", back_populates="product")

class Card(Base):
    __tablename__ = 'cards'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    is_active = Column(Integer, default=1)  
    
    
    products = relationship("CardProduct", back_populates="card")

class CardProduct(Base):
    __tablename__ = 'card_products'
    
    id = Column(Integer, primary_key=True)
    card_id = Column(Integer, ForeignKey('cards.id'))
    product_id = Column(Integer, ForeignKey('products.id'))
    quantity = Column(Integer)
    
    
    card = relationship("Card", back_populates="products")
    product = relationship("Product", back_populates="cards")

class Employee(Base):
    __tablename__ = 'employees'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    role = Column(String)  
    
    
    sales = relationship("Sale", back_populates="employee")

class Supplier(Base):
    __tablename__ = 'suppliers'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    
    
    products = relationship("Product", secondary=product_supplier, back_populates="suppliers")

class Sale(Base):
    __tablename__ = 'sales'

    id = Column(Integer, primary_key=True, index=True)
    total = Column(Float)
    employee_id = Column(Integer, ForeignKey('employees.id'))
    card_id = Column(Integer, ForeignKey('cards.id'))
    
    
    employee = relationship("Employee", back_populates="sales")
    card = relationship("Card"),
    products = relationship("Product", secondary=sale_product)