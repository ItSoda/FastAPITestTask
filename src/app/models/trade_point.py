from sqlalchemy import  Column, Integer, String
from src.database import Base


class TradePoint(Base):
    __tablename__ = "trade_point"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)


