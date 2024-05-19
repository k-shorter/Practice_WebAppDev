from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from db import Base

class Hotel(Base):
 __tablename__ = "hotel"
 id = Column(Integer, primary_key=True)
 name = Column(String(128))
 prefecture = Column(String(32))
 # room テーブルとの関連付け（1対多）
 rooms = relationship("Room", back_populates="hotel")

class Room(Base):
 __tablename__ = "room"
 id = Column(Integer, primary_key=True)
 name = Column(String(128))
 hotel_id = Column(Integer, ForeignKey('hotel.id'))
 # hotel テーブルとの関連付け
 hotel = relationship("Hotel", back_populates="rooms")