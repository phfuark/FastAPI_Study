from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import Table  # Ensure Table is imported
import uvicorn
from typing import List

from models import Base, Product, Card, Employee, Supplier, Sale, CardProduct, engine, sale_product  # Import sale_product
from schemas import (
    ProductCreate, ProductResponse, ProductUpdate,
    CardCreate, CardResponse, CardProductCreate, CardProductResponse,
    EmployeeCreate, EmployeeResponse,
    SupplierCreate, SupplierResponse,
    SaleCreate, SaleResponse
)

app = FastAPI()

Base.metadata.create_all(bind=engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get('/')
def hello_world():
    return {'message': 'E-Commerce System API'}

# Product Routes
@app.post('/products/', response_model=ProductResponse)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    db_product = Product(**product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

@app.get('/products/', response_model=List[ProductResponse])
def read_products(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(Product).offset(skip).limit(limit).all()

@app.get('/products/{product_id}', response_model=ProductResponse)
def read_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@app.put('/products/{product_id}', response_model=ProductResponse)
def update_product(product_id: int, product: ProductUpdate, db: Session = Depends(get_db)):
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    
    update_data = product.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_product, key, value)
    
    db.commit()
    db.refresh(db_product)
    return db_product

# Card Routes
@app.post('/cards/', response_model=CardResponse)
def create_card(card: CardCreate, db: Session = Depends(get_db)):
    db_card = Card(**card.model_dump())
    db.add(db_card)
    db.commit()
    db.refresh(db_card)
    return db_card

@app.get('/cards/', response_model=List[CardResponse])
def read_cards(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(Card).offset(skip).limit(limit).all()

@app.get('/cards/{card_id}', response_model=CardResponse)
def read_card(card_id: int, db: Session = Depends(get_db)):
    card = db.query(Card).filter(Card.id == card_id).first()
    if card is None:
        raise HTTPException(status_code=404, detail="Card not found")
    return card

@app.post('/cards/{card_id}/products/', response_model=CardProductResponse)
def add_product_to_card(
    card_id: int, 
    card_product: CardProductCreate, 
    db: Session = Depends(get_db)
):
    card = db.query(Card).filter(Card.id == card_id).first()
    if card is None:
        raise HTTPException(status_code=404, detail="Card not found")
    
    product = db.query(Product).filter(Product.id == card_product.product_id).first()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    
    existing_item = db.query(CardProduct).filter(
        CardProduct.card_id == card_id,
        CardProduct.product_id == card_product.product_id
    ).first()
    
    if existing_item:
        existing_item.quantity += card_product.quantity
    else:
        existing_item = CardProduct(
            card_id=card_id,
            product_id=card_product.product_id,
            quantity=card_product.quantity
        )
        db.add(existing_item)
    
    db.commit()
    db.refresh(existing_item)
    return existing_item

# Employee Routes
@app.post('/employees/', response_model=EmployeeResponse)
def create_employee(employee: EmployeeCreate, db: Session = Depends(get_db)):
    db_employee = Employee(**employee.model_dump())
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    return db_employee

@app.get('/employees/', response_model=List[EmployeeResponse])
def read_employees(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(Employee).offset(skip).limit(limit).all()

# Supplier Routes
@app.post('/suppliers/', response_model=SupplierResponse)
def create_supplier(supplier: SupplierCreate, db: Session = Depends(get_db)):
    db_supplier = Supplier(name=supplier.name)
    db.add(db_supplier)
    db.commit()
    db.refresh(db_supplier)
    
    for product_id in supplier.product_ids:
        product = db.query(Product).filter(Product.id == product_id).first()
        if product:
            db_supplier.products.append(product)
    
    db.commit()
    return db_supplier

@app.get('/suppliers/', response_model=List[SupplierResponse])
def read_suppliers(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    suppliers = db.query(Supplier).offset(skip).limit(limit).all()
    return suppliers

# Sale Routes
@app.post("/sales/", response_model=SaleResponse)
def create_sale(sale_data: dict, db: Session = Depends(get_db)):
    try:
        # Verifica se o funcionário e o cartão existem
        employee = db.query(Employee).filter(Employee.id == sale_data["employee_id"]).first()
        if not employee:
            raise HTTPException(status_code=404, detail="Employee not found")

        card = db.query(Card).filter(Card.id == sale_data["card_id"]).first()
        if not card:
            raise HTTPException(status_code=404, detail="Card not found")

        # Cria a venda
        new_sale = Sale(employee_id=sale_data["employee_id"], card_id=sale_data["card_id"], total=0.0)
        db.add(new_sale)
        db.commit()
        db.refresh(new_sale)

        total = 0.0

        # Associa os produtos à venda
        for item in sale_data.get("products", []):
            product = db.query(Product).filter(Product.id == item["product_id"]).first()
            if not product:
                raise HTTPException(status_code=404, detail=f"Product with ID {item['product_id']} not found")

            # Atualiza estoque
            if product.quantity < item["quantity"]:
                raise HTTPException(status_code=400, detail=f"Not enough stock for product {product.id}")

            product.quantity -= item["quantity"]
            total += product.price * item["quantity"]

            # Insere na tabela intermediária (sale_product)
            db.execute(sale_product.insert().values(sale_id=new_sale.id, product_id=product.id, quantity=item["quantity"]))

        # Atualiza o total da venda
        new_sale.total = total
        db.commit()
        db.refresh(new_sale)

        return new_sale  # Retorna a venda criada como resposta

    except Exception as e:
        db.rollback()
        print(f"Erro interno: {e}")
        raise HTTPException(status_code=500, detail="Erro interno ao processar a venda")
