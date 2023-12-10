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


class VisitCreate(BaseModel):
    destination_id: int
    author_id: int
    order_id: int
    worker_id: int


class VisitPartialUpdate(BaseModel):
    destination_id: Optional[int] = None
    order_id: Optional[int] = None
    worker_id: Optional[int] = None


class WorkerCreate(BaseModel):
    name: str
    phone: str
    trade_point_id: int


class WorkerPartialUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    trade_point_id: Optional[int] = None


class CustomerCreate(BaseModel):
    name: str
    phone: str
    trade_point_id: int


class CustomerPartialUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    trade_point_id: Optional[int] = None


class TradePointCreate(BaseModel):
    name: str


class TradePointPartialUpdate(BaseModel):
    name: Optional[str] = None
