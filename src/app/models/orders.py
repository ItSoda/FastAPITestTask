from datetime import datetime
from enum import Enum as PythonEnum

from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base


class OrderStatus(str, PythonEnum):
    """Table for order status"""

    started = "started"
    ended = "ended"
    in_proccess = "in proccess"
    awaiting = "awaiting"
    canceled = "canceled"


class Order(Base):
    """Table for order"""

    __tablename__ = "order"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    created_datetime: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    end_datetime: Mapped[datetime] = mapped_column(default=None)
    destination_id: Mapped[int] = mapped_column(
        ForeignKey("trade_point.id"), nullable=False
    )
    author_id: Mapped[int] = mapped_column(ForeignKey("customer.id"), nullable=False)
    status: Mapped[OrderStatus]
    worker_id: Mapped[int] = mapped_column(ForeignKey("worker.id"), nullable=False)

    destination = relationship("TradePoint", back_populates="orders")
    author = relationship("Customer", back_populates="orders")
    worker = relationship("Worker", back_populates="orders")
    visits = relationship("Visit", back_populates="order", cascade="all, delete-orphan")
