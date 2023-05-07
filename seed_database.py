import os
import json
from random import choice, redirect
from datetime import datetime


import crud
import model
import server

os.system("dropdb stocks")
os.system("createdb stocks")


model.connect_to_db(server.app)
model.db.create_all()

#Loads the stock data from the created JSON file
with open("data/stocks.json") as f:
    stock_data = json.loads(f.read())


#Create stocks, stores them in a list
stocks_in_db = []
for stock in stock_data:
    title, overview, purchase_price, industry_sector = (
        stock["title"],
        stock["overview"],
        stock["purchase_price"],
        stock["industry_sector"]
    )
    ipo_date = datetime.strptime(stock["ipo_date"], "%Y-%m-%d")

    db.stock = crud.create_stock(title, overview, ipo_date, purchase_price, industry_sector)
    stocks_in_db.append(db_stock)

# Create 15 users, each user will make 15 ratings
for n in range(15):
    email = f"user{n}@test.com"
    password = "test"

    user = crud.create_user(email, password)
    model.db.session.add(user)

    for _ in range(15):
        random_stock = choice(stocks_in_db)
        score = randint(1, 10)

        rating = crud.create_rating(user, random_stock, score)
        model.db.session.add(rating)

model.db.session.commit()