from flask import Flask, render_template, request, flash, session, redirect
from model import connect_to_db, db
import crud

from jinja2 import StrictUndefined

app = Flask(__name__)

app.secret_key = "this is my most secret key"

@app.route("/")
def homepage():
    """Look at the homepage."""

    return render_template("homepage.html")

@app.route("/stocks")
def all_stocks():
    """View all the stocks."""

    stocks = crud.get_stocks


@app.route("/users")
def all_users():
    """View the user."""

    users = crud.get_users()

    return render_template("all_users.hmtl", users=users)


@app.route("/users", methods=["POST"])
def register_user():
    """Create new user."""

    email = request.form.get("email")  ##Call email from for loop within seed database file 
    password = request.form.get("password")   ##call password from same for loop

    user = crud.get_user_by_email(email)
    if user:
        flash("We apologize that we are unable to create an account with that email. Please try again.")
    else:
        user = crud.create_user(email, password)
        db.session.add(user)
        db.session.commit()
        flash("Your account was created! Please log in.")

    return redirect("/")

@app.route("/users/<user_id>")
def show_user(user_id):
    """Show the details on a particular user."""

    user = crud.get_user_by_id(user_id)

    return render_template("user_details.html", user=user)


@app.route("/login", methods=["POST"])
def process_login():
    """Process a users login."""

    email = request.form.get("email")
    password = request.form.get("password")

    user = crud.get_user_by_email(email)
    if not user or user.password != password:
        flash("The email or password you have entered does not match!")
    else:
        #log in user by storing users email in session
        session["user_email"] = user.email
        flash(f"Glad to welcome you back, {user.email}!")

    return redirect("/")

@app.route("/update_rating", methods=["POST"])
def update_rating():
    rating_id = request.json["rating_id"]
    update_score = request.json["update_score"]
    crud.update_rating(rating_id, updated_score)
    db.session.commit()

    return "Success, YAY!"

@app.route("/stocks/<stock_id>/ratings", methods=["POST"])
def create_rating(stock_id):
    """Create a new rating for a stock."""

    logged_in_email = session.get("user_email")
    rating_score = request.form.get("rating")

    if logged_in_email is None:
        flash("You need to be logged in to rate a stock.")
    elif not rating_score:
        flash("Error: you did not select a score for your rating.")
    else:
        user = crud.get_user_by_email(logged_in_email)
        stock = crud.get_stock_by_id(stock_id)

        rating = crud.create_rating(user, stock, int(rating_score))
        db.session.add(rating)
        db.session.commit()

        flash(f"You have rated this stock {rating_score} out of 10.")

    return redirect(f"/stocks/{stock_id}")

#@app.route()


if __name__ == "__main__":
    connect_to_db(app)
    app.run(port=8080, debug=True)