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
        from_attributes = True

# Card schemas
class CardBase(BaseModel):
    name: str

class CardCreate(CardBase):
    pass

class CardResponse(CardBase):
    id: int
    is_active: bool
    
    class Config:
        from_attributes = True

class CardProductBase(BaseModel):
    product_id: int
    quantity: int

class CardProductCreate(CardProductBase):
    pass

class CardProductResponse(CardProductBase):
    id: int
    product: ProductResponse
    
    class Config:
        from_attributes = True

# Employee schemas
class EmployeeBase(BaseModel):
    name: str
    role: str

class EmployeeCreate(EmployeeBase):
    pass

class EmployeeResponse(EmployeeBase):
    id: int
    
    class Config:
        from_attributes = True

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
        from_attributes = True

# Sale schemas
class SaleBase(BaseModel):
    employee_id: int
    card_id: int
    products: List[CardProductBase] = []

class SaleCreate(SaleBase):
    pass

class SaleProductResponse(BaseModel):
    product_id: int
    name: str
    price: float
    quantity: int

class SaleResponse(BaseModel):
    id: int
    total: float
    employee: EmployeeResponse
    products: List[SaleProductResponse]
    
    class Config:
        from_attributes = True