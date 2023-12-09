from sqlalchemy import  Column, ForeignKey, Integer, String
from src.database import Base
from sqlalchemy.orm import relationship

class TradePoint(Base):
    __tablename__ = "trade_point"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)

    workers = relationship("Worker", back_populates="trade_point")
    customers = relationship("Customer", back_populates="trade_point")
    orders = relationship("Order", back_populates="destination")
