from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from src.database import Base


class TradePoint(Base):
    """Table for TradePoint"""

    __tablename__ = "trade_point"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)

    workers = relationship("Worker", back_populates="trade_point")
    customers = relationship("Customer", back_populates="trade_point")
    orders = relationship("Order", back_populates="destination")
