from datetime import datetime
from enum import Enum as PythonEnum

from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer
from sqlalchemy.orm import relationship

from src.database import Base


class OrderStatus(str, PythonEnum):
    """Table for Order Status"""

    started = "started"
    ended = "ended"
    in_proccess = "in proccess"
    awaiting = "awaiting"
    canceled = "canceled"


class Order(Base):
    """Table for order"""

    __tablename__ = "order"

    id = Column(Integer, primary_key=True, index=True)
    created_datetime = Column(DateTime, default=datetime.utcnow)
    end_datetime = Column(DateTime)
    destination_id = Column(Integer, ForeignKey("trade_point.id"), nullable=False)
    author_id = Column(Integer, ForeignKey("customer.id"), nullable=False)
    status = Column(Enum(OrderStatus))
    worker_id = Column(Integer, ForeignKey("worker.id"), nullable=False)

    destination = relationship("TradePoint", back_populates="orders")
    author = relationship("Customer", back_populates="orders")
    worker = relationship("Worker", back_populates="orders")
    visits = relationship("Visit", back_populates="order", cascade="all, delete-orphan")
