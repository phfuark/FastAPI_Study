from pydantic import BaseModel
from typing import List, Optional

# Product schemas
class ProductBase(BaseModel):
    name: str
    description: str
    price: float
    quantity: int

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    quantity: Optional[int] = None

class ProductResponse(ProductBase):
    id: int
    
    class Config:
        orm_mode = True

# Card schemas
class CardBase(BaseModel):
    name: str

class CardCreate(CardBase):
    pass

class CardResponse(CardBase):
    id: int
    is_active: bool
    
    class Config:
        orm_mode = True

class CardProductBase(BaseModel):
    product_id: int
    quantity: int

class CardProductCreate(CardProductBase):
    pass

class CardProductResponse(CardProductBase):
    id: int
    product: ProductResponse
    
    class Config:
        orm_mode = True

# Employee schemas
class EmployeeBase(BaseModel):
    name: str
    role: str

class EmployeeCreate(EmployeeBase):
    pass

class EmployeeResponse(BaseModel):
    id: int
    name: str
    role: str

# Supplier schemas
class SupplierBase(BaseModel):
    name: str
    product_ids: List[int] = []

class SupplierCreate(SupplierBase):
    pass

class SupplierResponse(SupplierBase):
    id: int
    products: List[ProductResponse] = []
    
    class Config:
        orm_mode = True

# Sale schemas
class SaleCreate(BaseModel):
    employee_id: int
    card_id: int
    products: List[dict]  # A list of product dictionaries containing product_id and quantity

class SaleResponse(BaseModel):
    id: int
    total: float
    employee: EmployeeResponse
    products: List[ProductResponse]

    class Config:
        orm_mode = True
