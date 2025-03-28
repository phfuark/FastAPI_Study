from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
import uuid

app = FastAPI()

# MODELS ================

class Item(BaseModel):
    name: str
    price: float
    description: str

# URLS ==================

@app.get("/")
def read_root():
    return {"Hello": "World"}

# GET ----------------------

@app.get("/items/{item_name}")
def read_item(item_name: str, item_description: Optional[str] = None, item_price: Optional[float] = None):
    item = {
        "name": item_name,
        "description": item_description,
        "price": item_price
    }
    return item

# POST ----------------------

@app.post('/create_item/')
async def create_item(item: Item):
    item.id = str(uuid.uuid4())
    return item

# PUT ----------------------

@app.put('/items/{item_id}/')
async def update_item(item_id: str, item: Item):
    return {
        'item_id': item_id,
        'item_name': item.name,
        'item_price': item.price,
        'item_description': item.description
    }

# # DELETE --------------------

# @app.delete('/items/{item_id}/')
# async def delete_item(item_id: int):
    