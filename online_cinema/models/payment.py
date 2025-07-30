from sqlalchemy import Column, Integer, ForeignKey, DateTime, Enum, Numeric, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from online_cinema.db.base_class import Base

class PaymentStatus(str, enum.Enum):
    successful = "successful"
    canceled = "canceled"
    refunded = "refunded"

class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    status = Column(Enum(PaymentStatus), nullable=False, default=PaymentStatus.successful)
    amount = Column(Numeric(10, 2), nullable=False)
    external_payment_id = Column(String, nullable=True)

    user = relationship("User", back_populates="payments")
    order = relationship("Order", back_populates="payments")
    items = relationship("PaymentItem", back_populates="payment", cascade="all, delete-orphan")

class PaymentItem(Base):
    __tablename__ = "payment_items"

    id = Column(Integer, primary_key=True, index=True)
    payment_id = Column(Integer, ForeignKey("payments.id"), nullable=False)
    order_item_id = Column(Integer, ForeignKey("order_items.id"), nullable=False)
    price_at_payment = Column(Numeric(10, 2), nullable=False)

    payment = relationship("Payment", back_populates="items")
    order_item = relationship("OrderItem", back_populates="payment_items")
