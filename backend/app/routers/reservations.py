from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

import models
import schemas

from db import get_db

router = APIRouter()

@router.post("/reservations/", response_model=schemas.Reservation)
def create_reservation(reservation_data: schemas.ReservationCreate, db: Session = Depends(get_db)):
    try:
        # 利用可能席数を取得
        availability = db.query(models.Availability).filter(models.Availability.restaurant_id == reservation_data.restaurant_id).first()
        if not availability or availability.available_seats < reservation_data.reserved_seats:
            raise HTTPException(status_code=400, detail="利用可能な席数が足りません。")

        # 予約を作成
        reservation_dict = reservation_data.dict()
        reservation_dict['reservation_date'] = datetime.utcnow()
        reservation_dict['updated_at'] = datetime.utcnow()
        db_reservation = models.Reservation(**reservation_dict)
        db.add(db_reservation)

        # 利用可能席数を更新
        availability.available_seats -= reservation_data.reserved_seats
        db.add(availability)

        db.commit()
        db.refresh(db_reservation)
        return db_reservation
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")