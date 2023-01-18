from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    ForeignKey,
    Boolean,
    JSON,
    Date,
    Float
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import random


Base = declarative_base()
engine = create_engine("sqlite:///foodstuffs.db")


class Restaurants(Base):
    __tablename__ = "Restaurants"

    rid = Column("rid", Integer, primary_key=True)
    name = Column("name", String)
    manager = Column("manager", String)
    username = Column("username", String)
    password = Column("password", String)
    address = Column("address", String)
    date_donated = Column("date_donated", Date)


class Food(Base):
    __tablename__ = "Food"

    fid = Column("fid", Integer, primary_key=True)
    restaurant = Column("restaurant", Integer, ForeignKey("Restaurants.rid"), nullable=False)
    food_name = Column("food_name", String)
    quantity = Column("quantity", Integer)
    date_donated = Column("date_donated", Date)
    expiry_date = Column("expiry_date", Date)
    category = Column("category", String)
    weight = Column("weight", Float)
    calories = Column("calories", Integer)
    takenby = Column("takenby", Integer)

class FoodBanks(Base):
    __tablename__ = "FoodBanks"

    fbid = Column("fbid", Integer, primary_key=True)
    foodBank = Column("FoodBank", String)
    username = Column("username", String)
    password = Column("password", String)
    address = Column("address", String)



Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
