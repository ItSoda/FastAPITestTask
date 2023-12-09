from typing import List
from fastapi import APIRouter, Depends, HTTPException

from .models.workers import Worker
from .models.customers import Customer
from .models.orders import Order
from .dependencies import get_db
from sqlalchemy.orm import Session
from .models.trade_point import TradePoint
from .schemas import OrderList, OrderUpdate, OrderCreate, OrderUpdateStatus, TradePointList, OrderPartialUpdate

router_trade_point = APIRouter(
    prefix="/trade_point",
    tags=["trade_point"]
)


# Task 1
@router_trade_point.get("/")
async def trade_point_list(phone: str, db: Session = Depends(get_db)):
    try:
        worker = db.query(Worker).filter(Worker.phone == phone).first()
        if worker:
            trade_points = db.query(TradePoint).join(Worker).filter(Worker.phone == phone).order_by(TradePoint.name).all()
            return {
                "status": 200, 
                "data": trade_points, 
                "detail": "Trade points list"
                }
        else:
            raise HTTPException(status_code=404, detail="Worker not found")
    except:
        raise HTTPException(status_code=500, detail="There is the exception")
    

# CRUD ORDER Task 2

router_order = APIRouter(
    prefix="/order",
    tags=["order"]
    )


@router_order.get("/")
def order_list(phone: str, db: Session = Depends(get_db)):
    try:
        customer = db.query(Customer).filter(Customer.phone == phone).first()
        if customer:
            orders = db.query(Order).join(Customer).filter(Customer.id == customer.id).order_by(Order.created_datetime).all()
            return {
                "status": 200,
                "data": orders,
                "detail": "Order list successfully"
                }
        else:
            raise HTTPException(status_code=404, detail="Customer not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"There is the exception {str(e)}")


@router_order.post("/create")
def order_create(order_data: OrderCreate, phone: str, db: Session = Depends(get_db)):
    try:
        customer = db.query(Customer).filter(Customer.phone == phone).first()
        worker = db.query(Worker).filter(Worker.id == order_data.worker_id).first()

        if customer:
            trade_point = db.query(TradePoint).join(Customer).join(Worker).filter(Customer.id == customer.id, Worker.id == worker.id).first()
            order = Order(author_id=customer.id, destination_id=order_data.destination_id, status=order_data.status, worker_id=order_data.worker_id)
            db.add(order)
            db.commit()
            db.refresh(order)
            return {
                "status": 201,
                "data": order,
                "detail": "Order created successfully"
            }
        else:
            raise HTTPException(status_code=404, detail="Customer not found")
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"There is the exception {str(e)}")


@router_order.put("/update_order/{order_id}")
def order_update(order_data: OrderUpdate, order_id: int, phone: str, db: Session = Depends(get_db)):
    try:
        customer = db.query(Customer).filter(Customer.phone == phone).first()

        if customer:
            trade_point = db.query(TradePoint).join(Customer).join(Worker).filter(Customer.id == customer.id, Worker.id == order_data.worker_id).first()
            if trade_point.id == order_data.destination_id:
                order = db.query(Order).filter(Order.id == order_id).first()
                if order:
                    for key, value in order_data.dict().items():
                        setattr(order, key, value)
                    db.commit()
                    db.refresh(order)
                    return {
                        "status": 200,
                        "data": order,
                        "detail": "Order update successfully"
                        }
                else:
                    raise HTTPException(status_code=404, detail="Order not found")
            else:
                raise HTTPException(status_code=404, detail="TradePoint is bad")
        else:
            raise HTTPException(status_code=404, detail="Customer not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"There is the exception {str(e)}")


@router_order.put("/update_order_status/{order_id}")
def order_update_status(order_data: OrderUpdateStatus, order_id: int, phone: str, db: Session = Depends(get_db)):
    try:
        customer = db.query(Customer).filter(Customer.phone == phone).first()

        if customer:
            order = db.query(Order).filter(Order.id == order_id).first()
            if order:
                order.status = order_data.status
                db.commit()
                db.refresh(order)
                return {
                    "status": 200,
                    "data": order,
                    "detail": "Order status update successfully"
                    }
            else:
                raise HTTPException(status_code=404, detail="Order not found")
        else:
            raise HTTPException(status_code=404, detail="Customer not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"There is the exception {str(e)}")


@router_order.patch("/update/{order_id}")
def order_patch(phone: str, order_id: int, order_data: OrderPartialUpdate, db: Session = Depends(get_db)):
    try:
        order = db.query(Order).get(order_id)
        if order:
            trade_point = db.query(TradePoint).get(order.destination_id)
            if order_data.status is not None:
                order.status = order_data.status

            if order_data.worker_id is not None:
                worker = db.query(Worker).filter(Worker.id == order_data.worker_id).first()
                customer = db.query(Customer).filter(Customer.id == order.author_id).first()
                if worker.trade_point_id == customer.trade_point_id:
                    order.worker_id = order_data.worker_id
                else:
                    raise HTTPException(status_code=404, detail="Worker is bad")
            if order_data.destination_id is not None:
                order.destination_id = order_data.destination_id

            if order_data.created_datetime is not None:
                order.created_datetime = order_data.created_datetime

            if order_data.end_datetime is not None:
                order.end_datetime = order_data.end_datetime

            db.commit()
            db.refresh(order)

            return {
                "status": 200,
                "data": order,
                "detail": "Order updated successfully"
            }
        else:
            raise HTTPException(status_code=404, detail="Order not found")
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"There is the exception {str(e)}")


@router_order.delete("/delete_order/{order_id}")
def order_delete(order_id: int, phone: str, db: Session = Depends(get_db)):
    try:
        customer = db.query(Customer).filter(Customer.phone == phone).first()
        if customer:
            order = db.query(Order).get(order_id)
            db.delete(order)
            db.commit()
            return {
                "status": 200,
                "data": [],
                "detail": "Order delete successfully"
                }
        else:
            raise HTTPException(status_code=404, detail="Customer not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"There is the exception {str(e)}")

