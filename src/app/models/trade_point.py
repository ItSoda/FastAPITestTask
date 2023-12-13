from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base


class TradePoint(Base):
    """Table for TradePoint"""

    __tablename__ = "trade_point"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)

    workers = relationship("Worker", back_populates="trade_point")
    customers = relationship("Customer", back_populates="trade_point")
    orders = relationship("Order", back_populates="destination")
