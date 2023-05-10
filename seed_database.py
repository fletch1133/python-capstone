import os
import json
# from random import choice, redirect
from flask import Flask, redirect
# from flask import Flask
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from model import Stock, db, connect_to_db
# import crud


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['POSTGRES_URI']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
connect_to_db(app)

# db = SQLAlchemy(app)


os.system("dropdb project-capstone-app")
os.system("createdb project-capstone-app")

# create the application context
with app.app_context():
    print('I called app_context')
    db.create_all()
    with open("/Users/anthonyfletcher/Ex from specs/Capstone/data/stocks.json") as f:
        stock_data = json.loads(f.read())
        print(f'i found {stock_data.count} stocks')
        db.session.add_all(stock_data)
        db.session.commit()
        





# # model.connect_to_db(server.app)
# # model.db.create_all()

# #Loads the stock data from the created JSON file
#3


# #Create stocks, stores them in a list
# stocks_in_db = []
# for stock in stock_data:
#     title, overview, purchase_price, industry_sector = (
#         stock["title"],
#         stock["overview"],
#         stock["purchase_price"],
#         stock["industry_sector"]
#     )
#     # ipo_date = datetime.strptime(stock["ipo_date"], "%Y-%m-%d")
#     ipo_date = datetime.strptime(stock["ipo_date"], "%B %d, %Y")

#     db.stock = crud.create_stock(id, title, overview, ipo_date, purchase_price, industry_sector)
#     stocks_in_db.append(db.stock)

# Create 15 users, each user will make 15 ratings
# for n in range(15):
#     email = f"user{n}@test.com"
#     password = "test"

#     user = crud.create_user(email, password)
#     model.db.session.add(user)

#     for _ in range(15):
#         random_stock = choice(stocks_in_db)
#         score = randint(1, 10)

#         rating = crud.create_rating(user, random_stock, score)
#         model.db.session.add(rating)

# model.db.session.commit()