from pydantic import BaseModel
from typing import List
from datetime import datetime

class CartItemBase(BaseModel):
    movie_id: int

class CartItemCreate(CartItemBase):
    pass

class CartItemRead(CartItemBase):
    id: int
    added_at: datetime

    class Config:
        orm_mode = True

class CartBase(BaseModel):
    user_id: int

class CartCreate(CartBase):
    pass

class CartRead(CartBase):
    id: int
    items: List[CartItemRead] = []

    class Config:
        orm_mode = True
