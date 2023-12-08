from datetime import datetime
from sqlalchemy import  Column, Integer, ForeignKey, DateTime, Enum
from enum import Enum as PythonEnum
from src.database import Base


class OrderStatus(str, PythonEnum):
    started = "started"
    ended = "ended"
    in_proccess = "in proccess"
    awaiting = "awaiting"
    canceled = "canceled"


class Order(Base):
    __tablename__ = "order"

    id = Column(Integer, primary_key=True, index=True)
    created_datetime = Column(DateTime, default=datetime.utcnow)
    end_datetime = Column(DateTime)
    destination_id = Column(Integer, ForeignKey("trade_point.id"), nullable=False)
    author_id = Column(Integer, ForeignKey("customer.id"), nullable=False)
    status = Column(Enum(OrderStatus))
    worker_id = Column(Integer, ForeignKey("worker.id"), nullable=False)
