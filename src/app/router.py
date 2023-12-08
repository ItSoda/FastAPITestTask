from fastapi import APIRouter, Depends, HTTPException

from .models.workers import Worker
from .dependencies import get_db
from sqlalchemy.orm import Session
from .models.trade_point import TradePoint


router = APIRouter(
    prefix="/trade_point",
    tags=["trade_point"]
)

@router.get("/{phone}")
async def trade_point_list(phone:str, session: Session = Depends(get_db)):
    worker = session.query(Worker).filter(Worker.phone == phone).first()

    if not worker:
        raise HTTPException(status_code=404, detail="worker not found")

    trade_points = session.query(TradePoint).filter(TradePoint.id == worker.trade_point_id).all()
    return {
        "status": 200, 
        "data": trade_points, 
        "detail": None
        }

