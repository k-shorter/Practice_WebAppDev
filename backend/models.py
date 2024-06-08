from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Float, Boolean, Time, LargeBinary
from sqlalchemy.orm import relationship
from db import Base

class User(Base):
    __tablename__ = 'user'
    user_id = Column(Integer, primary_key=True)
    user_name = Column(String(255))

    organizer = relationship("Organizer", back_populates="user", uselist=False)
    participants = relationship("Participant", back_populates="user", uselist=False)
    preference = relationship("Preference", back_populates="user", uselist=False)

class Organizer(Base):
    __tablename__ = 'organizer'
    organizer_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.user_id'))

    user = relationship("User", back_populates="organizer")
    event = relationship("Event", back_populates="organizer", uselist=False)
    reservations = relationship("Reservation", back_populates="organizer")

class Participant(Base):
    __tablename__ = 'participant'
    participant_id = Column(Integer, primary_key=True)
    is_attending = Column(Boolean)
    user_id = Column(Integer, ForeignKey('user.user_id'))
    event_id = Column(Integer, ForeignKey('event.event_id'))

    user = relationship("User", back_populates="participants")
    event = relationship("Event", back_populates="participants", uselist=False)
    payment = relationship("Payment", back_populates="participant", uselist=False)

class Event(Base):
    __tablename__ = 'event'
    event_id = Column(Integer, primary_key=True)
    event_name = Column(String(255))
    event_date = Column(DateTime)
    total_cost = Column(Float)
    primary_participant_count = Column(Integer)
    secondary_participant_count = Column(Integer)
    latitude = Column(Float)
    longitude = Column(Float)
    organizer_id = Column(Integer, ForeignKey('organizer.organizer_id'))

    organizer = relationship("Organizer", back_populates="event")
    participants = relationship("Participant", back_populates="event")

class Payment(Base):
    __tablename__ = 'payment'
    payment_id = Column(Integer, primary_key=True)
    amount = Column(Float)
    payment_date = Column(DateTime)
    payment_status = Column(Integer)
    updated_at = Column(DateTime)
    participant_id = Column(Integer, ForeignKey('participant.participant_id'))
    payment_method_id = Column(Integer, ForeignKey('payment_method.payment_method_id'))

    participant = relationship("Participant", back_populates="payment")
    payment_method = relationship("PaymentMethod", back_populates="payments")

class PaymentMethod(Base):
    __tablename__ = 'payment_method'
    payment_method_id = Column(Integer, primary_key=True)
    method_name = Column(String(255))

    payments = relationship("Payment", back_populates="payment_method")

class Preference(Base):
    __tablename__ = 'preference'
    preference_id = Column(Integer, primary_key=True)
    genre = Column(String(255))
    smoking_allowed = Column(Boolean)
    budget = Column(Float)
    additional_info = Column(String(255))
    user_id = Column(Integer, ForeignKey('user.user_id'))

    user = relationship("User", back_populates="preference")

class Restaurant(Base):
    __tablename__ = 'restaurant'
    restaurant_id = Column(Integer, primary_key=True)
    restaurant_name = Column(String(255))
    address = Column(String(255))
    contact = Column(String(255))
    total_seats = Column(Integer)
    latitude = Column(Float)
    longitude = Column(Float)
    image = Column(String(500)) 

    restaurant_details = relationship("RestaurantDetails", back_populates="restaurant", uselist=False)
    availability = relationship("Availability", back_populates="restaurant", uselist=False)
    reservations = relationship("Reservation", back_populates="restaurant")

class RestaurantDetails(Base):
    __tablename__ = 'restaurant_details'
    restaurant_details_id = Column(Integer, primary_key=True)
    genre = Column(String(255))
    smoking_allowed = Column(Boolean)
    budget = Column(Float)
    additional_info = Column(String(255))
    restaurant_id = Column(Integer, ForeignKey('restaurant.restaurant_id'))

    restaurant = relationship("Restaurant", back_populates="restaurant_details")

class Availability(Base):
    __tablename__ = 'availability'
    availability_id = Column(Integer, primary_key=True)
    available_seats = Column(Integer)
    updated_at = Column(DateTime)
    restaurant_id = Column(Integer, ForeignKey('restaurant.restaurant_id'))

    restaurant = relationship("Restaurant", back_populates="availability")

class Reservation(Base):
    __tablename__ = 'reservation'
    reservation_id = Column(Integer, primary_key=True)
    reservation_date = Column(DateTime)
    reserved_seats = Column(Integer)
    reservation_status = Column(Integer)
    arrival_time = Column(DateTime)
    updated_at = Column(DateTime)
    restaurant_id = Column(Integer, ForeignKey('restaurant.restaurant_id'))
    organizer_id = Column(Integer, ForeignKey('organizer.organizer_id'))

    restaurant = relationship("Restaurant", back_populates="reservations")
    organizer = relationship("Organizer", back_populates="reservations")