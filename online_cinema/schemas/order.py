from pydantic import BaseModel
from typing import List
from datetime import datetime
from enum import Enum

class OrderStatus(str, Enum):
    pending = "pending"
    paid = "paid"
    canceled = "canceled"

class OrderItemBase(BaseModel):
    movie_id: int
    price_at_order: float

class OrderItemCreate(OrderItemBase):
    pass

class OrderItemRead(OrderItemBase):
    id: int

    class Config:
        orm_mode = True

class OrderBase(BaseModel):
    user_id: int
    status: OrderStatus = OrderStatus.pending
    total_amount: float = 0.0

class OrderCreate(OrderBase):
    items: List[OrderItemCreate]

class OrderRead(OrderBase):
    id: int
    created_at: datetime
    items: List[OrderItemRead] = []

    class Config:
        orm_mode = True
