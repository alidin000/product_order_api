from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class ProductBase(BaseModel):
    """Base model for Product"""
    name: str
    description: Optional[str] = None 
    price: float
    quantity: int

class ProductCreate(ProductBase):
    pass

class Product (ProductBase):
    id: int

    class Config:
        orm_mode = True

class OrderItemBase(BaseModel):
    product_id: int
    quantity: int

    class Config:
        orm_mode = True
        from_attributes = True

class OrderBase(BaseModel):
    status: str

class OrderCreate(BaseModel):
    items: List[OrderItemBase]

class Order(BaseModel):
    id: int
    created_at: datetime
    status: str
    items: List[OrderItemBase]

    class Config:
        orm_mode = True
        from_attributes = True


class OrderStatusUpdate(BaseModel):
    status: str