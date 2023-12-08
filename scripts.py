from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from faker import Faker
import random
from src.config import DB_HOST, DB_NAME, DB_PASSWORD, DB_PORT, DB_USER
from src.app.models.orders import Order, OrderStatus
from src.app.models.visits import Visit
from src.database import engine
from src.app.models.workers import Worker
from src.app.models.customers import Customer
from src.app.models.trade_point import TradePoint

fake = Faker()


def create_entities(db_session):
    for _ in range(500):
        worker = Worker(
            name=fake.name(),
            phone=fake.phone_number(),

        )
        db_session.add(worker)

    for _ in range(15):
        customer = Customer(
            name=fake.name(),
            phone=fake.phone_number(),

        )
        db_session.add(customer)

    for _ in range(10000):
        trade_point = TradePoint(
            name=fake.name(),
            workers=random.randint(1, 499),
            customers=random.randint(16, 30)
        )
        db_session.add(trade_point)


    for _ in range(500):
        order = Order(
            created_datetime=fake.date_time_this_decade(),
            end_datetime=fake.date_time_this_decade(),
            destination_id=fake.random_int(min=5, max=14),
            author_id=random.randint(16, 30),
            status=random.choice(list(OrderStatus)),
            worker_id=random.randint(5, 500),
        )
        db_session.add(order)

    for _ in range(150):
        visit = Visit(
            created_datetime=fake.date_time_this_decade(),
            worker_id=random.randint(5, 500),
            order_id=fake.random_int(min=5, max=435),
            destination_id=fake.random_int(min=5, max=14),
            author_id=random.randint(16, 30),
        )
        db_session.add(visit)

    db_session.commit()

if __name__ == "__main__":
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    with SessionLocal() as db:
        create_entities(db)