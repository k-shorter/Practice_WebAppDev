from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
import models
import schemas
from db import get_db
from math import ceil

router = APIRouter()

@router.post("/participants/")
def create_participant(participant_data: schemas.ParticipantCreate, db: Session = Depends(get_db)):
    try:
        # ユーザーの作成
        new_user = models.User(**participant_data.user.dict())
        db.add(new_user)
        db.flush() 
        
        # イベント情報の確認
        event = db.query(models.Event).filter(models.Event.event_id == participant_data.event_id).first()
        if not event:
            raise HTTPException(status_code=404, detail="Event not found.")
        
        # 参加者の作成
        new_participant = models.Participant(
            is_attending=participant_data.is_attending,
            user_id=new_user.user_id,
            event_id=event.event_id,
        )
        db.add(new_participant)
        db.flush() 

        # 支払い情報の計算と登録
        amount = round(event.total_cost / max(event.primary_participant_count, 1))
        new_payment = models.Payment(
            **participant_data.payment.dict(exclude={"amount"}),
            amount=ceil(amount),
            participant_id=new_participant.participant_id
        )
        db.add(new_payment)

        # 好みの登録
        new_preference = models.Preference(**participant_data.preference.dict(), user_id=new_user.user_id)
        db.add(new_preference)
        db.commit()
        db.refresh(new_participant)

        participant_with_relations = db.query(models.Participant).options(
            joinedload(models.Participant.user).joinedload(models.User.preference),
            joinedload(models.Participant.event),
            joinedload(models.Participant.payment)
        ).filter(models.Participant.participant_id == new_participant.participant_id).first()

        return participant_with_relations
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@router.post("/adjust_participants/", response_model=schemas.Event)
def adjust_participants(data: schemas.AdjustParticipants, db: Session = Depends(get_db)):
    try:
        # イベント情報を取得
        event = db.query(models.Event).filter(models.Event.event_id == data.event_id).first()
        if not event:
            raise HTTPException(status_code=404, detail="Event not found.")
        
        # イベントに紐づく参加者の合計数を取得し、num_people_adjustmentを考慮して更新
        participant_count = db.query(models.Participant).filter(models.Participant.event_id == event.event_id).count()
        total_count = participant_count + data.num_people_adjustment
        event.secondary_participant_count = total_count
        db.commit()

        return event
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
