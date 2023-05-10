from flask import Flask, render_template, request, flash, session, redirect, url_for
from model import connect_to_db, db
import crud
import json


from jinja2 import StrictUndefined

app = Flask(__name__)

app.secret_key = "this is my most secret key"

@app.route("/")
def homepage():
    """Look at the homepage."""

    return render_template("homepage.html")

#@app.route("/stocks")
#def all_stocks():
   # """View all the stocks."""

    #stocks = crud.get_stocks()

@app.route("/stocks")
def all_stocks():
    with open('/Users/anthonyfletcher/Ex from specs/Capstone/data/stocks.json') as f:
        stocks = json.load(f)
    return render_template("all_stocks.html", stocks=stocks)



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

# @app.route("/stocks/<stock_title>/<rating>", methods=["POST"])
# def create_rating(stock_title, rating):
#     print(stock_title, rating)
#     print(request.form)
#     """Create a new rating for a stock."""
#     flash(f"You rated {stock_title} as {rating} stock!")
#     return redirect(url_for("stocks"))


@app.route("/stocks", methods=["POST"])
def create_rating():
    """Create a new rating for a stock."""
    user = crud.get_user_by_email(session['user_email'])
    if(user is None):
        user = crud.get_user_by_id(1)
    crud.create_rating(stock_id=request.form.get("stock-selector"), user_id=user.id, score=request.form.get("values-selector"))
    #flash(f"You rated {request.form.get("stock-selector")} as {rating} stock!")
    return redirect(url_for("all_stocks"))


@app.route("/update_rating", methods=["POST"])
def update_rating():
    rating_id = request.json["rating_id"]
    update_score = request.json["update_score"]
    crud.update_rating(rating_id, update_score)
    db.session.commit()

    flash(f"You have updated the rating")
    return render_template("all_stocks.html", rating_id=rating_id, update_score=update_score)


@app.route("/")
def messages(MessageForm):
    messages = []
    senders = User.query.all()
    message_form = MessageForm()
    message_form.recipient.choices = [(user.id, user.username) for user in User.query.all()]


    sender_id = request.args.get('sender')
    if sender_id is not None:
        messages = crud.get_all_messages(sender_id=int(sender_id))
    else:
        messages = crud.get_all_messages()

    if message_form.validate_on_submit():
        sender_id = current_user.id
        recipient_id = int(message_form.recipient.data)
        message = message_form.message.data
        new_message = Message(sender_id=sender_id, recipient_id=recipient_id, message=message)
        db.session.add(new_message)
        db.session.commit()
        flash('Message sent!')

    sender_id = request.args.get('sender')

    if sender_id:
        messages = crud.get_all_messages(sender_id=int(sender_id), recipient_id=current_user.id)
    else:
        messages = crud.get_all_messages(recipient_id=current_user.id)


    return render_template('messages.html', message_form=message_form, messages=messages, senders=senders)


if __name__ == "__main__":
    connect_to_db(app)
    app.run(port=8080, debug=True)