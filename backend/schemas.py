from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

#ユーザーの基本情報
class UserBase(BaseModel):
    user_name: str="user_name"

class UserCreate(UserBase):
    pass

class User(UserBase):
    user_id: int

    class Config:
        orm_mode = True

#参加者登録用
class PreferenceBase(BaseModel):
    genre: str="海鮮, 中華, イタリアン, 焼き鳥"
    smoking_allowed: bool
    budget: float
    additional_info: Optional[str] = None

class PreferenceCreate(PreferenceBase):
    pass

class Preference(PreferenceBase):
    preference_id: int
    user_id: int

    class Config:
        orm_mode = True

class PaymentBase(BaseModel):
    payment_method_id: int=1
    payment_date: datetime
    payment_status: int
    updated_at: datetime

class PaymentCreate(PaymentBase):
    pass

class Payment(PaymentBase):
    payment_id: int
    amount: float
    participant_id: int

    class Config:
        orm_mode = True

class ParticipantBase(BaseModel):
    is_attending: bool

class ParticipantCreate(ParticipantBase):
    user: UserCreate
    event_id: int=1
    payment: PaymentCreate
    preference: PreferenceCreate

class Participant(ParticipantBase):
    participant_id: int
    user: User
    event_id: int
    payment: Payment
    preference: Preference

    class Config:
        orm_mode = True

#イベント作成用
class OrganizerBase(BaseModel):
    user: UserCreate

class OrganizerCreate(OrganizerBase):
    pass

class Organizer(OrganizerBase):
    organizer_id: int
    user: User

    class Config:
        orm_mode = True

class EventBase(BaseModel):
    event_name: str="event_name"
    event_date: datetime
    total_cost: float=45000
    primary_participant_count: int=8
    secondary_participant_count: int
    latitude: float=35.6951
    longitude: float=139.7536

class EventCreate(EventBase):
    organizer: OrganizerCreate

class Event(EventBase):
    event_id: int
    organizer: Organizer

    class Config:
        orm_mode = True

#参加者数調整用
class AdjustParticipants(BaseModel):
    event_id: int=1
    num_people_adjustment: int=-1

    class Config:
        orm_mode = True

#参加者数調整用
class SearchRestaurant(BaseModel):
    event_id: int=1
    budget: float=2000
    class Config:
        orm_mode = True
        