from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from enum import Enum

class PaymentStatus(str, Enum):
    successful = "successful"
    canceled = "canceled"
    refunded = "refunded"

class PaymentItemBase(BaseModel):
    order_item_id: int
    price_at_payment: float

class PaymentItemCreate(PaymentItemBase):
    pass

class PaymentItemRead(PaymentItemBase):
    id: int

    class Config:
        orm_mode = True

class PaymentBase(BaseModel):
    user_id: int
    order_id: int
    status: PaymentStatus = PaymentStatus.successful
    amount: float
    external_payment_id: Optional[str] = None

class PaymentCreate(PaymentBase):
    items: List[PaymentItemCreate]

class PaymentRead(PaymentBase):
    id: int
    created_at: datetime
    items: List[PaymentItemRead] = []

    class Config:
        orm_mode = True
