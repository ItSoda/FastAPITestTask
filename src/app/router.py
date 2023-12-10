from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .dependencies import get_db
from .models.customers import Customer
from .models.orders import Order
from .models.trade_point import TradePoint
from .models.visits import Visit
from .models.workers import Worker
from .schemas import (
    CustomerCreate,
    CustomerPartialUpdate,
    OrderCreate,
    OrderPartialUpdate,
    OrderUpdate,
    OrderUpdateStatus,
    TradePointCreate,
    TradePointPartialUpdate,
    VisitCreate,
    VisitPartialUpdate,
    WorkerCreate,
    WorkerPartialUpdate,
)

router_trade_point = APIRouter(prefix="/trade_point", tags=["trade_point"])


# Task 1
@router_trade_point.get("/worker_trade_point")
def trade_point_list_worker(phone: str, db: Session = Depends(get_db)):
    try:
        worker = db.query(Worker).filter(Worker.phone == phone).first()
        if worker:
            trade_points = (
                db.query(TradePoint)
                .join(Worker)
                .filter(Worker.phone == phone)
                .order_by(TradePoint.name)
                .all()
            )
            return {"status": 200, "data": trade_points, "detail": "Trade points list"}
        else:
            raise HTTPException(status_code=404, detail="Worker not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"There is the exception {str(e)}")


@router_trade_point.get("/")
def trade_point_list(phone: str, db: Session = Depends(get_db)):
    customer = db.query(Customer).filter(Customer.phone == phone).first()
    if customer:
        trade_point_list = db.query(TradePoint).all()
        return {
            "status": 200,
            "data": trade_point_list,
            "detail": "TradePoint list successfully",
        }
    else:
        raise HTTPException(status_code=404, detail="Customer not found")


@router_trade_point.post("/create_trade_point")
def trade_point_post(
    phone: str, trade_point_data: TradePointCreate, db: Session = Depends(get_db)
):
    customer = db.query(Customer).filter(Customer.phone == phone).first()
    if customer:
        trade_point = TradePoint(**trade_point_data.dict())
        db.add(trade_point)
        db.commit()
        db.refresh(trade_point)
        return {
            "status": 201,
            "data": trade_point,
            "detail": "TradePoint create successfully",
        }
    else:
        raise HTTPException(status_code=404, detail="Customer not found")


@router_trade_point.patch("/partial_update_trade_point/{trade_point_id}")
def trade_point_partial_udpate(
    phone: str,
    trade_point_id: int,
    trade_point_data: TradePointPartialUpdate,
    db: Session = Depends(get_db),
):
    customer = db.query(Customer).filter(Customer.phone == phone).first()
    trade_point = db.query(TradePoint).filter(TradePoint.id == trade_point_id).first()

    if customer:
        if trade_point_data.name is not None:
            trade_point.name = trade_point_data.name
        db.commit()
        db.refresh(trade_point)
        return {
            "status": 200,
            "data": trade_point,
            "detail": "TradePoint partial update successfully",
        }
    else:
        raise HTTPException(status_code=404, detail="Customer not found")


@router_trade_point.delete("/delete_trade_point/{trade_point_id}")
def trade_point_delete(phone: str, trade_point_id: int, db: Session = Depends(get_db)):
    customer = db.query(Customer).filter(Customer.phone == phone).first()
    trade_point = db.query(TradePoint).filter(TradePoint.id == trade_point_id).first()
    if customer:
        if trade_point:
            order_instance = (
                db.query(Order).filter(Order.destination_id == trade_point.id).first()
            )
            if order_instance is None:
                db.delete(trade_point)
                db.commit()
                return {
                    "status": 200,
                    "data": [],
                    "detail": "TradePoint delete successfully",
                }
            else:
                raise HTTPException(status_code=404, detail="Delete the order first")
        else:
            raise HTTPException(status_code=404, detail="TradePoint not found")
    else:
        raise HTTPException(status_code=404, detail="Customer not found")


# Search for name
@router_trade_point.get("/search_trade_point/{name}")
def trade_point_list_name(phone: str, name: str, db: Session = Depends(get_db)):
    customer = db.query(Customer).filter(Customer.phone == phone).first()
    if customer:
        trade_point = db.query(TradePoint).filter(TradePoint.name == name).all()
        return {
            "status": 200,
            "data": trade_point,
            "detail": f"TradePoint with name {name}",
        }
    else:
        raise HTTPException(status_code=404, detail="Customer not found")


# CRUD ORDER Task 2

router_order = APIRouter(prefix="/order", tags=["order"])


@router_order.get("/")
def order_list(phone: str, db: Session = Depends(get_db)):
    try:
        customer = db.query(Customer).filter(Customer.phone == phone).first()
        if customer:
            orders = (
                db.query(Order)
                .join(Customer)
                .filter(Customer.id == customer.id)
                .order_by(Order.created_datetime)
                .all()
            )
            return {"status": 200, "data": orders, "detail": "Order list successfully"}
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
            trade_point = (
                db.query(TradePoint)
                .join(Customer)
                .join(Worker)
                .filter(Customer.id == customer.id, Worker.id == worker.id)
                .first()
            )
            if trade_point:
                order = Order(
                    author_id=customer.id,
                    destination_id=order_data.destination_id,
                    status=order_data.status,
                    worker_id=order_data.worker_id,
                )
                db.add(order)
                db.commit()
                db.refresh(order)
                return {
                    "status": 201,
                    "data": order,
                    "detail": "Order created successfully",
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
def order_update(
    order_data: OrderUpdate, order_id: int, phone: str, db: Session = Depends(get_db)
):
    try:
        customer = db.query(Customer).filter(Customer.phone == phone).first()

        if customer:
            trade_point = (
                db.query(TradePoint)
                .join(Customer)
                .join(Worker)
                .filter(Customer.id == customer.id, Worker.id == order_data.worker_id)
                .first()
            )
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
                        "detail": "Order update successfully",
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
def order_update_status(
    order_data: OrderUpdateStatus,
    order_id: int,
    phone: str,
    db: Session = Depends(get_db),
):
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
                    "detail": "Order status update successfully",
                }
            else:
                raise HTTPException(status_code=404, detail="Order not found")
        else:
            raise HTTPException(status_code=404, detail="Customer not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"There is the exception {str(e)}")


@router_order.patch("/partial_update/{order_id}")
def order_patch(
    phone: str,
    order_id: int,
    order_data: OrderPartialUpdate,
    db: Session = Depends(get_db),
):
    try:
        order = db.query(Order).get(order_id)
        if order:
            if order_data.status is not None:
                order.status = order_data.status

            if order_data.worker_id is not None:
                worker = (
                    db.query(Worker).filter(Worker.id == order_data.worker_id).first()
                )
                customer = (
                    db.query(Customer).filter(Customer.id == order.author_id).first()
                )
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
                "detail": "Order updated successfully",
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
            return {"status": 200, "data": [], "detail": "Order delete successfully"}
        else:
            raise HTTPException(status_code=404, detail="Customer not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"There is the exception {str(e)}")


# CRUD VISITS TASK 4
router_visit = APIRouter(prefix="/visit", tags=["Visit"])


@router_visit.get("/")
def visit_list(phone: str, db: Session = Depends(get_db)):
    try:
        customer = db.query(Customer).filter(Customer.phone == phone).first()

        if not customer:
            raise HTTPException(status_code=404, detail="Customer not found")

        visits = db.query(Visit).join(Customer).filter(Customer.phone == phone).all()
        return {"status": 200, "data": visits, "detail": "Visits list successfully"}
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
        raise HTTPException(
            status_code=404, detail="Visit with Order has already been created"
        )

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
        return {"status": 201, "data": visit, "detail": "Visit create successfully"}


@router_visit.put("/update_visit/{visit_id}")
def visit_update(
    phone: str, visit_id: int, visit_data: VisitCreate, db: Session = Depends(get_db)
):
    customer = db.query(Customer).filter(Customer.phone == phone).first()
    visit = db.query(Visit).filter(Visit.id == visit_id).first()

    if validate_visit(customer=customer, visit_data=visit_data, db=db):
        for key, value in visit_data.dict().items():
            setattr(visit, key, value)
        db.commit()
        db.refresh(visit)
        return {"status": 200, "data": visit, "detail": "Visit update successfully"}


@router_visit.patch("/partial_update_visit/{visit_id}")
def visit_partial_update(
    phone: str,
    visit_id: int,
    visit_data: VisitPartialUpdate,
    db: Session = Depends(get_db),
):
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
            visit_test = (
                db.query(Visit)
                .join(Order)
                .filter(Order.id == visit_data.order_id)
                .first()
            )
            if visit_test:
                raise HTTPException(
                    status_code=404, detail="Visit with Order has already been created"
                )
            visit.order_id = visit_data.order_id
        db.commit()
        db.refresh(visit)

        return {
            "status": 200,
            "data": visit,
            "detail": "Order partial update successfully",
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
            return {"status": 200, "data": [], "detail": "Visit delete successfully"}
        else:
            raise HTTPException(status_code=404, detail="Customer not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"There is the exception {str(e)}")


# TASK ADMIN
router_worker = APIRouter(prefix="/worker", tags=["worker"])


@router_worker.get("/")
def worker_list(phone: str, db: Session = Depends(get_db)):
    customer = db.query(Customer).filter(Customer.phone == phone).first()
    if customer:
        worker = db.query(Worker).all()
        return {"status": 200, "data": worker, "detail": "Worker list successfully"}
    else:
        raise HTTPException(status_code=404, detail="Customer not found")


@router_worker.post("/create_worker")
def worker_post(phone: str, worker_data: WorkerCreate, db: Session = Depends(get_db)):
    customer = db.query(Customer).filter(Customer.phone == phone).first()
    if customer:
        worker = Worker(**worker_data.dict())
        db.add(worker)
        db.commit()
        db.refresh(worker)
        return {"status": 201, "data": worker, "detail": "Worker create successfully"}
    else:
        raise HTTPException(status_code=404, detail="Customer not found")


@router_worker.patch("/partial_update_worker/{worker_id}")
def worker_partial_udpate(
    phone: str,
    worker_id: int,
    worker_data: WorkerPartialUpdate,
    db: Session = Depends(get_db),
):
    customer = db.query(Customer).filter(Customer.phone == phone).first()
    worker = db.query(Worker).filter(Worker.id == worker_id).first()

    if customer:
        if worker_data.name is not None:
            worker.name = worker_data.name
        if worker_data.phone is not None:
            worker.phone = worker_data.phone
        if worker_data.trade_point_id is not None:
            worker.trade_point_id = worker_data.trade_point_id
        db.commit()
        db.refresh(worker)
        return {
            "status": 200,
            "data": worker,
            "detail": "Worker partial update successfully",
        }
    else:
        raise HTTPException(status_code=404, detail="Customer not found")


@router_worker.delete("/delete_worker/{worker_id}")
def worker_delete(phone: str, worker_id: int, db: Session = Depends(get_db)):
    customer = db.query(Customer).filter(Customer.phone == phone).first()
    worker = db.query(Worker).filter(Worker.id == worker_id).first()

    if customer:
        if worker:
            db.delete(worker)
            db.commit()
            return {"status": 200, "data": [], "detail": "Worker delete successfully"}
        else:
            raise HTTPException(status_code=404, detail="Worker not found")
    else:
        raise HTTPException(status_code=404, detail="Customer not found")


# Search for name
@router_worker.get("/search_worker/{name}")
def worker_list_name(phone: str, name: str, db: Session = Depends(get_db)):
    customer = db.query(Customer).filter(Customer.phone == phone).first()
    if customer:
        worker = db.query(Worker).filter(Worker.name == name).all()
        return {"status": 200, "data": worker, "detail": f"Worker with name {name}"}
    else:
        raise HTTPException(status_code=404, detail="Customer not found")


# Search for phone
@router_worker.get("/search_worker/{phone_worker}")
def worker_list_phone(phone: str, phone_worker: str, db: Session = Depends(get_db)):
    customer = db.query(Customer).filter(Customer.phone == phone).first()
    if customer:
        worker = db.query(Worker).filter(Worker.phone == phone).all()
        return {
            "status": 200,
            "data": worker,
            "detail": f"Worker with name {phone_worker}",
        }
    else:
        raise HTTPException(status_code=404, detail="Customer not found")


router_customer = APIRouter(prefix="/customer", tags=["customer"])


@router_customer.get("/")
def customer_list(phone: str, db: Session = Depends(get_db)):
    customer = db.query(Customer).filter(Customer.phone == phone).first()
    if customer:
        customer_list = db.query(Customer).all()
        return {
            "status": 200,
            "data": customer_list,
            "detail": "Customer list successfully",
        }
    else:
        raise HTTPException(status_code=404, detail="Customer not found")


@router_customer.post("/create_customer")
def customer_post(
    phone: str, customer_data: CustomerCreate, db: Session = Depends(get_db)
):
    customer = db.query(Customer).filter(Customer.phone == phone).first()
    if customer:
        customer_instance = Customer(**customer_data.dict())
        db.add(customer_instance)
        db.commit()
        db.refresh(customer_instance)
        return {
            "status": 201,
            "data": customer_instance,
            "detail": "Customer create successfully",
        }
    else:
        raise HTTPException(status_code=404, detail="Customer not found")


@router_customer.patch("/partial_update_customer/{customer_id}")
def customer_partial_update(
    phone: str,
    customer_id: int,
    customer_data: CustomerPartialUpdate,
    db: Session = Depends(get_db),
):
    customer = db.query(Customer).filter(Customer.phone == phone).first()
    customer_instance = db.query(Customer).filter(Customer.id == customer_id).first()

    if customer:
        if customer_data.name is not None:
            customer_instance.name = customer_data.name
        if customer_data.phone is not None:
            customer_instance.phone = customer_data.phone
        if customer_data.trade_point_id is not None:
            customer_instance.trade_point_id = customer_data.trade_point_id
        db.commit()
        db.refresh(customer_instance)
        return {
            "status": 200,
            "data": customer_instance,
            "detail": "Customer partial update successfully",
        }
    else:
        raise HTTPException(status_code=404, detail="Customer not found")


@router_customer.delete("/delete_customer/{customer_id}")
def customer_delete(phone: str, customer_id: int, db: Session = Depends(get_db)):
    customer = db.query(Customer).filter(Customer.phone == phone).first()
    customer_instance = db.query(Customer).filter(Customer.id == customer_id).first()

    if customer:
        if customer_instance:
            db.delete(customer_instance)
            db.commit()
            return {"status": 200, "data": [], "detail": "Customer delete successfully"}
        else:
            raise HTTPException(status_code=404, detail="Customer_instance not found")
    else:
        raise HTTPException(status_code=404, detail="Customer not found")
