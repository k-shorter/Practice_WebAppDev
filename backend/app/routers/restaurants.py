from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
import models
import schemas

from db import get_db
from ..utils.distance import classify_restaurants_by_walking_time
from ..utils.budget import classify_restaurants_by_budget
from ..utils.preferences import classify_restaurants_by_preferences
from ..utils.best import find_best_restaurant

router = APIRouter()

@router.get("/search/restaurants_by_walking_time/", response_model=List[schemas.Restaurant])
def get_restaurants_by_walking_time(event_id: int = Query(..., description="Event ID"), db: Session = Depends(get_db)):
    event = db.query(models.Event).filter(models.Event.event_id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found.")
    
    available_restaurants = db.query(models.Restaurant).join(
        models.Availability,
        models.Restaurant.restaurant_id == models.Availability.restaurant_id
    ).filter(
        models.Availability.available_seats >= event.secondary_participant_count
    ).all()

    user_location = (event.latitude, event.longitude)
    restaurants_grouped_by_walking_time = classify_restaurants_by_walking_time(user_location, available_restaurants)
    
    return restaurants_grouped_by_walking_time

@router.get("/search/restaurants_by_budget/", response_model=List[schemas.Restaurant])
def get_restaurants_by_budget(
    event_id: int = Query(..., description="Event ID"),
    budget: int = Query(..., description="Specified budget"),
    db: Session = Depends(get_db)
):
    event = db.query(models.Event).filter(models.Event.event_id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found.")
    
    available_restaurants = db.query(models.Restaurant).join(
        models.Availability,
        models.Restaurant.restaurant_id == models.Availability.restaurant_id
    ).filter(
        models.Availability.available_seats >= event.secondary_participant_count
    ).all()
    
    restaurants_grouped_by_budget = classify_restaurants_by_budget(available_restaurants, budget)
    
    return restaurants_grouped_by_budget

@router.get("/search/restaurants_by_preferences/", response_model=List[schemas.Restaurant])
def get_restaurants_by_preferences(event_id: int = Query(..., description="Event ID"), db: Session = Depends(get_db)):
    event = db.query(models.Event).filter(models.Event.event_id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found.")
    
    available_restaurants = db.query(models.Restaurant).join(
        models.Availability,
        models.Restaurant.restaurant_id == models.Availability.restaurant_id
    ).filter(
        models.Availability.available_seats >= event.secondary_participant_count
    ).all()

    # 参加者の好みを取得
    participant_preferences = db.query(models.Preference).join(models.User).join(models.Participant).filter(models.Participant.event_id == event_id).all()

    # レストランを評価し、評価に基づいて分類する
    restaurants_grouped_by_preferences = classify_restaurants_by_preferences(available_restaurants, participant_preferences)

    return restaurants_grouped_by_preferences



@router.get("/search/best_restaurants/")
def get_best_restaurants(event_id: int = Query(..., description="Event ID"), budget: int = Query(..., description="Specified budget"), db: Session = Depends(get_db)):
    event = db.query(models.Event).filter(models.Event.event_id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found.")
    
    available_restaurants = db.query(models.Restaurant).join(
        models.Availability,
        models.Restaurant.restaurant_id == models.Availability.restaurant_id
    ).filter(
        models.Availability.available_seats >= event.secondary_participant_count
    ).all()

    user_location = (event.latitude, event.longitude)
    participant_preferences = db.query(models.Preference).join(models.User).join(models.Participant).filter(models.Participant.event_id == event_id).all()
    
    best_restaurants = find_best_restaurant(user_location, available_restaurants, budget, participant_preferences)

    return best_restaurants