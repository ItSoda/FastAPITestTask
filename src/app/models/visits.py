from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base


class Visit(Base):
    """Table for visit"""

    __tablename__ = "visit"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    created_datetime: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    destination_id: Mapped[int] = mapped_column(
        ForeignKey("trade_point.id"), nullable=False
    )
    author_id: Mapped[int] = mapped_column(ForeignKey("customer.id"), nullable=False)
    order_id: Mapped[int] = mapped_column(ForeignKey("order.id"), nullable=False)
    worker_id: Mapped[int] = mapped_column(ForeignKey("worker.id"), nullable=False)

    order = relationship("Order", back_populates="visits")
