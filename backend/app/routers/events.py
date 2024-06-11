from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session,joinedload

from typing import List
from datetime import datetime

import models
import schemas
from db import get_db

router = APIRouter()

@router.get("/events/{event_id}", response_model=schemas.Event)
def get_event(event_id: int, db: Session = Depends(get_db)):
    event = db.query(models.Event).filter(models.Event.event_id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event

@router.get("/events/{event_id}/participants", response_model=List[schemas.Participant])
def get_event_participants(event_id: int, db: Session = Depends(get_db)):
    participants = db.query(models.Participant).join(models.User).join(models.Preference).filter(models.Participant.event_id == event_id).all() 
    if not participants:
        raise HTTPException(status_code=404, detail="No participants found for the event")
    return participants

@router.post("/events/", response_model=schemas.Event)
def create_event(event_data: schemas.EventCreate, db: Session = Depends(get_db)):
    try:
        # イベントを作成
        event_dict = event_data.dict(exclude={"organizer"})
        event_dict['event_date'] = datetime.utcnow()
        new_event = models.Event(**event_dict)
        db.add(new_event)
        
        # Create organizer (user)
        organizer_data = event_data.organizer
        organizer_user = models.User(**organizer_data.user.dict())
        db.add(organizer_user)
        
        # Link event and organizer
        new_organizer = models.Organizer(user=organizer_user, event=new_event)
        db.add(new_organizer)
        
        db.commit()
        db.refresh(new_event)
        return new_event
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"An error occurred: {str(e)}")
    
@router.get("/events/{event_id}/reservations", response_model=schemas.Reservation)
def get_reservations_by_event(event_id: int, db: Session = Depends(get_db)):
    event = db.query(models.Event).filter(models.Event.event_id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found.")

    organizer = db.query(models.Organizer).filter(models.Organizer.organizer_id == event.organizer_id).first()
    if not organizer:
        raise HTTPException(status_code=404, detail="Organizer not found.")

    reservations = db.query(models.Reservation).options(
        joinedload(models.Reservation.restaurant)
    ).filter(models.Reservation.organizer_id == organizer.organizer_id).first()

    if not reservations:
        raise HTTPException(status_code=404, detail="No reservations found for this event.")
    
    return reservations
    
