from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base


class Customer(Base):
    """Table for customer"""

    __tablename__ = "customer"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    phone: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    trade_point_id: Mapped[int] = mapped_column(
        ForeignKey("trade_point.id"), nullable=False
    )

    trade_point = relationship("TradePoint", back_populates="customers")
    orders = relationship("Order", back_populates="author")
