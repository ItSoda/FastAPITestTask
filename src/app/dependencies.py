from src.database import session


# Зависимость с бд
def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()
