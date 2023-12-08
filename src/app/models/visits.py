from datetime import datetime
from sqlalchemy import  Column, Integer, ForeignKey, DateTime

from src.database import Base


class Visit(Base):
    __tablename__ = "visit"

    id = Column(Integer, primary_key=True, index=True)
    created_datetime = Column(DateTime, default=datetime.utcnow)
    destination_id = Column(Integer, ForeignKey("trade_point.id"), nullable=False)
    author_id = Column(Integer, ForeignKey("customer.id"), nullable=False)
    order_id = Column(Integer, ForeignKey("order.id"), nullable=False)
    worker_id = Column(Integer, ForeignKey("worker.id"), nullable=False)