from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel


class OrderType(str, Enum):
    started = "started"
    ended = "ended"
    in_proccess = "in proccess"
    awaiting = "awaiting"
    canceled = "canceled"


class OrderList(BaseModel):
    id: int
    created_datetime: datetime
    end_datetime: datetime
    destination_id: int
    worker_id: int
    author_id: int
    status: OrderType

class OrderUpdate(BaseModel):
    end_datetime: datetime
    destination_id: int
    worker_id: int
    status: OrderType


class OrderUpdateStatus(BaseModel):
    status: OrderType


class OrderPartialUpdate(BaseModel):
    created_datetime: Optional[str] = None
    end_datetime: Optional[str] = None
    destination_id: Optional[int] = None
    worker_id: Optional[int] = None
    status: Optional[str] = None



class OrderCreate(BaseModel):
    destination_id: int
    worker_id: int
    status: OrderType


class TradePointList(BaseModel):
    id: int
    name: str
    workers: str
    customers: str