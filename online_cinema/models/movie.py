from sqlalchemy import Column, Integer, String, Text, Numeric
from sqlalchemy.orm import relationship
from online_cinema.db.base_class import Base

class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    price = Column(Numeric(10, 2), nullable=False)

    cart_items = relationship("CartItem", back_populates="movie")
    order_items = relationship("OrderItem", back_populates="movie")
