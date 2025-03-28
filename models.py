from pydantic import BaseModel
from typing import Optional

class ProductCreate(BaseModel):
    name: str
    description: str
    price: float

class ProductResponse(BaseModel):
    id: int
    name: str
    description: str
    price: float

    # Essa configuração permite que o Pydantic leia os dados do modelo SQLAlchemy
    class Config:
        from_attributes = True

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None