from typing import List
from fastapi import APIRouter, Depends, HTTPException
from datetime import datetime
from .models.workers import Worker
from .models.customers import Customer
from .models.orders import Order
from .dependencies import get_db
from sqlalchemy.orm import Session
from .models.trade_point import TradePoint
from .models.visits import Visit
from .schemas import OrderList, OrderUpdate, OrderCreate, OrderUpdateStatus, TradePointList, OrderPartialUpdate, VisitCreate, VisitPartialUpdate

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


@router_order.post("/create_order")
def order_create(order_data: OrderCreate, phone: str, db: Session = Depends(get_db)):
    try:
        customer = db.query(Customer).filter(Customer.phone == phone).first()
        worker = db.query(Worker).filter(Worker.id == order_data.worker_id).first()

        if customer:
            trade_point = db.query(TradePoint).join(Customer).join(Worker).filter(Customer.id == customer.id, Worker.id == worker.id).first()
            if trade_point:
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
                raise HTTPException(status_code=404, detail="TradePoint not found")
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


# TASK 4 PUT ORDER STATUS
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


@router_order.patch("/partial_update/{order_id}")
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


# CRUD VISITS TASK 4
router_visit = APIRouter(
    prefix="/visit",
    tags=["Visit"]
    )

@router_visit.get("/")
def visit_list(phone: str, db: Session = Depends(get_db)):
    try:
        customer = db.query(Customer).filter(Customer.phone == phone).first()

        if not customer:
            raise HTTPException(status_code=404, detail="Customer not found")
        
        visits = db.query(Visit).join(Customer).filter(Customer.phone == phone).all()
        return {
            "status": 200,
            "data": visits,
            "detail": "Visits list successfully"
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"There is the exception {str(e)}")


def validate_visit(customer, visit_data, db):
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    if customer.id != visit_data.author_id:
        raise HTTPException(status_code=404, detail="Customer is not Author")

    if customer.trade_point_id != visit_data.destination_id:
        raise HTTPException(status_code=404, detail="TradePoint not found")
        
    order = db.query(Order).filter(Order.id == visit_data.order_id).first()
    if order.end_datetime < datetime.utcnow():
        raise HTTPException(status_code=404, detail="Order time is end")
        
    visit = db.query(Visit).join(Order).filter(Order.id == order.id).first()
    if visit:
        raise HTTPException(status_code=404, detail="Visit with Order has already been created")
        
    if order.worker_id != visit_data.worker_id:
        raise HTTPException(status_code=404, detail="The wrong worker")
    
    return True


@router_visit.post("/create_visit")
def visit_create(phone: str, visit_data: VisitCreate, db: Session = Depends(get_db)):
    customer = db.query(Customer).filter(Customer.phone == phone).first()

    if validate_visit(customer=customer, visit_data=visit_data, db=db):
        visit = Visit(**visit_data.dict())
        db.add(visit)
        db.commit()
        db.refresh(visit)
        return {
            "status": 201,
            "data": visit,
            "detail": "Visit create successfully"
        }


@router_visit.put("/update_visit/{visit_id}")
def visit_update(phone: str, visit_id: int, visit_data: VisitCreate, db: Session = Depends(get_db)):
    customer = db.query(Customer).filter(Customer.phone == phone).first()
    visit = db.query(Visit).filter(Visit.id == visit_id).first()

    if validate_visit(customer=customer, visit_data=visit_data, db=db):
        for key, value in visit_data.dict().items():
            setattr(visit, key, value)
        db.commit()
        db.refresh(visit)
        return {
            "status": 200,
            "data": visit,
            "detail": "Visit update successfully"
        }


@router_visit.patch("/partial_update_visit/{visit_id}")
def visit_partial_update(phone: str, visit_id: int, visit_data: VisitPartialUpdate, db: Session = Depends(get_db)):
    customer = db.query(Customer).filter(Customer.phone == phone).first()
    visit = db.query(Visit).filter(Visit.id == visit_id).first()

    if visit:
        if visit_data.destination_id is not None:
            if customer.trade_point_id == visit_data.destination_id:
                visit.destination_id = visit_data.destination_id

        if visit_data.worker_id is not None:
            worker = db.query(Worker).filter(Worker.id == visit_data.worker_id).first()
            order = db.query(Order).join(Worker).filter(Worker.id == worker.id).first()
            if worker.trade_point_id == customer.trade_point_id:
                if order.id == visit.order_id:
                    visit.worker_id = visit_data.worker_id
            else:
                raise HTTPException(status_code=404, detail="Worker is bad")
        if visit_data.order_id is not None:
            visit_test = db.query(Visit).join(Order).filter(Order.id == visit_data.order_id).first()
            if visit_test:
                raise HTTPException(status_code=404, detail="Visit with Order has already been created")
            visit.order_id = visit_data.order_id
        db.commit()
        db.refresh(visit)

        return {
            "status": 200,
            "data": visit,
            "detail": "Order partial update successfully"
        }
    else:
        raise HTTPException(status_code=404, detail="Visit not found")
    

@router_visit.delete("/delete_visit/{visit_id}")
def visit_delete(visit_id: int, phone: str, db: Session = Depends(get_db)):
    try:
        customer = db.query(Customer).filter(Customer.phone == phone).first()
        if customer:
            visit = db.query(Visit).get(visit_id)
            db.delete(visit)
            db.commit()
            return {
                "status": 200,
                "data": [],
                "detail": "Visit delete successfully"
                }
        else:
            raise HTTPException(status_code=404, detail="Customer not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"There is the exception {str(e)}")


