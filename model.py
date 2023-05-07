import os
from flask_sqlalchemy import SQLAlchemy 
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key = True, autoincrement= True)
    username = db.Column(db.String(255), unique = True, nullable = False)
    password = db.Column(db.String(255), unique = False, nullable = False)

    def __init__(self, username, password):     #takes in two parameters, username and password and sets the corresponding instance variables
        self.username = username
        self.password = password

    def __repr__(self):
        return f"<User user_id={self.user_id} email={self.email}>"


class Account(db.Model):

    __tablename__ = "accounts"

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    stocks = db.Column(db.String(255), unique = True, nullable = False)
    returns = db.Column(db.String(255), nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable = False)

    def __init__(self, stocks, returns, user_id):
        self.stocks = stocks
        self.returns = returns
        self.user_id = user_id

    def __repr__(self):
        return f"Account account_id={self.account_id} stocks={self.stocks} returns={self.returns}"

class Favorite(db.Model):

    __tablename__ = "favorites"

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    selected = db.Column(db.Boolean, unique = True, nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable = False)

    def __init__(self, selected, user_id):
        self.selected = selected
        self.user_id = user_id

class Industry(db.Model):

    __tablename__ = "industries"

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    account_id = db.Column(db.Integer, db.ForeignKey("accounts.id"), nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable = False)
    favorite_id = db.Column(db.Integer, db.ForeignKey("favorites.id"), nullable = False)

    def __init__(self, account_id, user_id, favorite_id):
        self.account_id = account_id
        self.user_id = user_id
        self.favorite_id = favorite_id

class Rating(db.Model):

    __tablename__ = "ratings"

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable = False)
    industry_id = db.Column(db.Integer, db.ForeignKey("industries.id"), nullable = False)
    account_id = db.Column(db.Integer, db.ForeignKey("accounts.id"), nullable = False)

    def __init__(self, user_id, industry_id, account_id):
        self.user_id = user_id
        self.industry_id = industry_id
        self.account_id = account_id

class Future(db.Model):

    __tablename__ = "futures"

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    stock_price = db.Column(db.String(255), unique = False, nullable = False)
    stock_name = db.Column(db.String(255), unique = True, nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable = False)
    industry_id = db.Column(db.Integer, db.ForeignKey("industries.id"), nullable = False)

    def __init__(self, stock_price, stock_name, user_id, industry_id):
        self.stock_price = stock_price
        self.stock_name = stock_name
        self.user_id = user_id
        self.industry_id = industry_id


class Stock(db.Model):

    __tablename__ = "stocks"

    id = db.Column(db.Integer, primary_key= True, autoincrement= True)
    account_id = db.Column(db.Integer, db.ForeignKey("accounts.id"), nullable = False)
    favorite_id = db.Column(db.Integer, db.ForeignKey("favorites.id"), nullable = False)
    industry_id = db.Column(db.Integer, db.ForeignKey("industries.id"), nullable = False)
    rating_id = db.Column(db.Integer, db.ForeignKey("ratings.id"), nullable = False)
    future_id = db.Column(db.Integer, db.ForeignKey("futures.id"), nullable = False)


class Message(db.Model):

    __tablename__ = "messages"

    message_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    recipient_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    date_time = db.Column(db.DateTime, default=datetime.utcnow)
    message = db.Column(db.String, nullable=False)

    #sender = db.relationship('User', db.ForeignKey['sender.id'])
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    sender = db.relationship('User')
    recipient = db.relationship('User', db.ForeignKey['recipient.id'])

    def get_time(self):
        return self.timestamp.strftime("%b %d, %Y, %H:%M:%S")

    def __repr__(self):
        return f"<Message={self.message}"


def connect_to_db(app):
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["POSTGRES_URI"]
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    from flask import Flask
    app = Flask(__name__)
    connect_to_db(app)
    print("Connected to db...")