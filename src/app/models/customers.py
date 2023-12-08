from sqlalchemy import  Column, Integer, String

from src.database import Base


class Customer(Base):
    __tablename__ = "customer"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    phone = Column(String(255), nullable=False, unique=True)
