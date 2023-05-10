from model import db, User, Account, Favorite, Industry, Rating, Future, Message, Stock
from flask import current_app
import json

def create_user(email, password):
    """Make a new user and return it."""

    user = User(email=email, password=password)

    return user

#def get_user():
    #"""Return all the users."""

    #return User.query.all()

def get_users():
    """Return a list of all users."""
    return User.query.all()


def get_user_by_id(user_id):
    """Return a user by their primary key."""
   
    return User.query.get(user_id)


def get_user_by_email(email):
    """Return a user by their email."""
 
    return User.query.filter_by(email=email).first()  


#def get_user_by_email(email):
    #"""Return a user by their email."""

    #db.session.query(User).order_by(User.id)
    #return User.query.filter_by(User.email == email).first()

def create_account(stocks, returns):
    """Create a new account."""

    account = Account(stocks=stocks, returns=returns)

    return account

def get_account_by_id():
    """Return the account by the primary key."""

    return Account.query.get(account_id)

#def create_rating():
    #"""Create a rating from 1 to 10 for a stock"""

    #return Rating

def create_rating(stock_id, user_id, score):
    """Create a new rating in the database."""
    rating = Rating(stock_id=stock_id, user_id=user_id, score=score)
    db.session.add(rating)
    db.session.commit()
    
    return rating


def update_rating(rating_id, new_score):
    """Update a rating in the database."""
    
    rating = Rating.query.get(rating_id)
    
    if rating:
        rating.score = new_score
        db.session.commit()
        return True
    else:
        return False

def get_ratings_by_stock_id(stock_id):
    ratings = Rating.query.filter_by(stock_id=stock_id)

    return ratings



def create_favorite(selected):
    """Create a list of favorite stocks."""

    favorite = Favorite(selected=selected)

def update_favorite(favorite_id, new_selected):
    """Update a favorite stock using the selection of a user."""

    selected = Favorite.query.get(favorite_id)
    favorite.selected = new_selected

def create_industry():
    """Create a catalog of all the economic industries."""

    return industry


def create_future(stock_price, stock_name):
    """Create a list of what the user thinks of future predictions."""

    future = Future(stock_price=stock_price, stock_name=stock_name)

    return future


# def create_stock(title, overview, ipo_date, purchase_price, industry_sector):
#     stock = Stock(title=title, overview=overview, ipo_date=ipo_date, purchase_price=purchase_price, industry_sector=industry_sector)
#     db.session.add(stock)
#     db.session.commit()
#     return stock




# def create_stock(title, overview, ipo_date, purchase_price, industry_sector):
#     with app.app_context():
#         db = db.get()
#         stock = Stock(title=title, overview=overview, ipo_date=ipo_date, purchase_price=purchase_price, industry_sector=industry_sector)
#         db.session.add(stock)
#         db.session.commit()
#         return stock

def create_stock(id, title, overview, ipo_date, purchase_price, industry_sector):
    """Create a new stock."""
    stock = Stock(title=title, overview=overview, ipo_date=ipo_date, purchase_price=purchase_price, industry_sector=industry_sector)
    db.session.add(stock)
    db.session.commit()
    return stock





def pick_stock():
    """Pick any stock out of the avaiable ones listed."""

    return stock

def get_all_stocks():
    
    return db.session.execute(db.select(Stock).order_by(Stock.id))


def get_all_messages(sender_id=None, recipient_id=None):
    if sender_id is not None:
        return Message.query.filter_by(sender_id=sender_id,recipient_id=recipient_id).order_by(Message.date_time.desc().all())
    else:
        return Message.query.order_by(Message.date_time.desc()).all()


if __name__ == "__main__":
    from server import app

    connect_to_db(app)