from fastapi import APIRouter, Depends, HTTPException

from .models.workers import Worker
from .dependencies import get_db
from sqlalchemy.orm import Session
from .models.trade_point import TradePoint


router = APIRouter(
    prefix="/trade_point",
    tags=["trade_point"]
)


# Task 1
@router.get("/{phone}")
async def trade_point_list(phone:str, session: Session = Depends(get_db)):
    try:
        worker = session.query(Worker).filter(Worker.phone == phone).first()
        if worker:
            trade_points = session.query(TradePoint).filter(TradePoint.workers == worker.id).order_by(TradePoint.name).all()
            return {
                "status": 200, 
                "data": trade_points, 
                "detail": None
                }
        else:
            raise HTTPException(status_code=404, detail="worker not found")
    except:
        raise HTTPException(status_code=500, detail="there is the exception")