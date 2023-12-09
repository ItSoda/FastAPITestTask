from sqlalchemy import func
from sqlalchemy.orm import sessionmaker, Session
from faker import Faker
import random
from src.app.models.orders import Order, OrderStatus
from src.app.models.visits import Visit
from src.database import engine
from src.app.models.workers import Worker
from src.app.models.customers import Customer
from src.app.models.trade_point import TradePoint

fake = Faker()

def create_entities(db_session: Session):
    for _ in range(1000):
        trade_point = TradePoint(name=fake.name())
        db_session.add(trade_point)

    db_session.commit()

    for _ in range(100):
        random_trade_point = db_session.query(TradePoint).order_by(func.random()).first()
        worker = Worker(name=fake.name(), phone=fake.phone_number(), trade_point_id=random_trade_point.id)
        db_session.add(worker)

    for _ in range(100):
        random_trade_point = db_session.query(TradePoint).order_by(func.random()).first()
        customer = Customer(name=fake.name(), phone=fake.phone_number(), trade_point_id=random_trade_point.id)
        db_session.add(customer)

    db_session.commit()

    for _ in range(500):
        random_worker = db_session.query(Worker).order_by(func.random()).first()
        random_customer = db_session.query(Customer).order_by(func.random()).first()

        common_trade_point = TradePoint(name=fake.name())
        db_session.add(common_trade_point)
        db_session.commit()

        order = Order(
            created_datetime=fake.date_time_this_decade(),
            end_datetime=fake.date_time_this_decade(),
            destination_id=common_trade_point.id,
            author_id=random_customer.id,
            status=random.choice(list(OrderStatus)),
            worker_id=random_worker.id,
        )
        db_session.add(order)

    db_session.commit()

    for _ in range(150):
        random_worker = db_session.query(Worker).order_by(func.random()).first()
        random_customer = db_session.query(Customer).order_by(func.random()).first()

        common_trade_point = db_session.query(TradePoint).order_by(func.random()).first()

        random_order = db_session.query(Order).order_by(func.random()).first()

        visit = Visit(
            created_datetime=fake.date_time_this_decade(),
            destination_id=common_trade_point.id,
            author_id=random_customer.id,
            order_id=random_order.id,
            worker_id=random_worker.id,
        )
        db_session.add(visit)

    db_session.commit()

if __name__ == "__main__":
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    with SessionLocal() as db:
        create_entities(db)

# {
#     "destination_id": 75,
#     "status": "ended",
#     "end_datetime": "2023-12-10T21:00:59",
#     "worker_id": 43
# } 511