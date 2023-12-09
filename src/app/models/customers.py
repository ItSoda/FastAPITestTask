from sqlalchemy import  Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from src.database import Base


class Customer(Base):
    __tablename__ = "customer"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    phone = Column(String(255), nullable=False, unique=True)
    trade_point_id = Column(Integer, ForeignKey("trade_point.id"), nullable=False)

    trade_point = relationship("TradePoint", back_populates="customers")
    orders = relationship("Order", back_populates="author")
