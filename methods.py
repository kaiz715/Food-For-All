from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Boolean, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from db import Restaurants, Food, Session, FoodBanks
from datetime import date, timedelta
# from distance import all_distances
import random, time
import requests
import json

import os
import openai

openai.api_key = "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"

weightLimit = 0

api_key = "AIzaSyA6MlUm3WtJcWCkC57Otk8L50qm14O8R5k"

def find_restauants(source, radius, date):
    url ='https://maps.googleapis.com/maps/api/distancematrix/json?'
    # Get method of requests module
    # return response object
    session = Session()
    restaurants = session.query(Restaurants).all()
    restfilter = []
    # for restaurant in restaurants:
    #     r = requests.get(url + 'origins=' + source +
    #                     '&destinations=' + restaurant.address +
    #                     '&key=AIzaSyCiR_wNw04TUn0WCdJ7FHS-UF_6_fX4QVg')
    #     r = r.json()['rows'][0]['elements'][0]['distance']['value']/1000
    #     if r < radius:
    #         if restaurant.date_donated == date:
    #             restfilter.append(restaurant.rid)
    # session.close()
    for restaurant in restaurants:
        restfilter.append(restaurant.rid)
    return restfilter


def get_restaurant_info(rid):
    session = Session()
    restaurant = session.query(Restaurants).filter_by(rid = rid).first()
    info = {}
    info["name"] = restaurant.name
    info["address"] = restaurant.address
    info["date_donated"] = restaurant.date_donated
    session.close()
    return info


def get_food_info(fid):
    session = Session()
    food = session.query(Food).filter_by(fid = fid).first()
    info = {}
    info["food_name"] = food.food_name
    info["quantity"] = food.quantity
    info["date_donated"] = food.date_donated
    info["expiry_date"] = food.expiry_date
    info["category"] = food.category
    info["weight"] = food.weight
    info["calories"] = food.calories
    info["takenby"] = food.takenby
    session.close()
    return info

def get_foodBank_info(username):
    session = Session()
    foodBank = session.query(FoodBanks).filter_by(username = username).first()
    info = {}
    info["fbid"] = foodBank.fbid
    info["foodBank"] = foodBank.foodBank
    info["address"] = foodBank.address
    session.close()
    return info

def list_foods(rids): #based off of expiration and food eat time
    session = Session()
    restaurants = []
    for rid in rids:
        restaurants.append(session.query(Restaurants).filter_by(rid = rid).first())
    food_arr = []
    for restaurant in restaurants:
        food_arr.append([])
        foods = session.query(Food).filter_by(restaurant = restaurant.rid)
        for food in foods:
            if food.date_donated == date.today():
                food_arr[-1].append(get_food_info(food.fid))
    session.close()
    return food_arr


def add_restauant(restaurant_name, address, date):
    session = Session()
    restaurant = Restaurants()
    rid = next_id("Restaurants")
    restaurant.rid = rid
    restaurant.name = restaurant_name
    restaurant.address = address
    restaurant.date_donated = date
    session.add(restaurant)
    session.commit()
    session.close()
    return rid

def add_food(restaurant, food_name, quantity, expiry_date):
    session = Session()
    food = Food()
    food.fid = next_id("Food")
    food.restaurant = restaurant
    food.food_name = food_name
    food.quantity = quantity
    food.date_donated = date.today()
    food.expiry_date = expiry_date
    food.category = foodCategory(food_name)
    food.calories = foodCalories(food_name)
    food.weight = foodWeight(food_name, quantity)
    session.add(food)
    session.commit()
    session.close()

def foodCategory(food_name):
    prompt = f"Is an {food_name} a pastry, fruit, vegetable, dairy, drink, meat, canned food, or snack? output only one word"
    response = openai.Completion.create(

        model = "text-davinci-003",
        prompt = prompt,
        max_tokens = 20,
        temperature = 1.2,
        top_p = 1
    )
    # Extract the information you need from the response
    category = response['choices'][0]['text'][2:]
    return category

def foodWeight(food_name, quantity):
    # prompt = f"how much does 1 {food_name} weigh in pounds. only display number"
    # print(prompt)
    # response = openai.Completion.create(
    #     model = "text-davinci-003",
    #     prompt = prompt,
    #     max_tokens = 20,
    #     temperature = 0.1,
    #     top_p = 1
    # )
    # # Extract the information you need from the response
    # weight = response['choices'][0]['text'][3:]
    # return float(weight)*quantity
    return 3


def foodCalories(food_name):
    # prompt = f"how many calories does a {food_name} have. only output number"
    # response = openai.Completion.create(

    #     model = "text-davinci-003",
    #     prompt = prompt,
    #     max_tokens = 20,
    #     temperature = 0.8,
    #     top_p = 1
    # )
    # # Extract the information you need from the response
    # calories = response['choices'][0]['text']
    # return int(calories)
    return 300

def add_foodbank(org, username, password, address):
    session = Session()
    foodBank = FoodBanks()
    foodBank.fbid = next_id("FoodBanks")
    foodBank.foodBank = org
    foodBank.username = username
    foodBank.password = password
    foodBank.address = address
    session.add(foodBank)
    session.commit()
    session.close()

def check_org_credentials(username, password):
    session = Session()
    if session.query(FoodBanks).filter_by(username=username).first() != None and session.query(FoodBanks).filter_by(username=username).first().password == password:
        return True
    return False
    

def next_id(db):
    session = Session()
    if db == "Restaurants":
        first = session.query(func.max(Restaurants.rid)).first()[0]
    elif db == "Food":
        first = session.query(func.max(Food.fid)).first()[0]
    elif db == "FoodBanks":
        first = session.query(func.max(FoodBanks.fbid)).first()[0]
    session.close()

    if first != None:
        return first + 1
    else:
        return 0