from sqlalchemy import  Column, Integer, String, ForeignKey

from src.database import Base


class Worker(Base):
    __tablename__ = "worker"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    phone = Column(String(255), nullable=False, unique=True)
    trade_point_id = Column(Integer, ForeignKey("trade_point.id"), nullable=False)