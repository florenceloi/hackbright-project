from jinja2 import StrictUndefined

from flask import Flask, render_template, redirect, request, flash, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension

import jsonpickle

from model import (connect_to_db, 
                   db,
                   User,
                   Restaurant,
                   Category,
                   Review,
                   Restaurant_Category)

from api import yelp_client, gmaps_key

app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Raise an error if an undefined variable in Jinja2 is used.
app.jinja_env.undefined = StrictUndefined


###############################################################################
# Flask routes

@app.route('/home')
def index():
    """Homepage."""

    # Instantiate category dictionary using dictionary comprehension
    categories = [category.category 
                  for category in Category.query.order_by('category').all()]

    return render_template("home.html", gmaps_key=gmaps_key, categories=categories)

@app.route('/home.json')
def bear_info():
    """JSON information about restaurants."""

    # Instantiate restaurant dictionary using dictionary comprehension
    restaurants = {
        restaurant.restaurant_id: {
            "_name": restaurant.name,
            "address": restaurant.address,
            "phone": restaurant.phone,
            "yelpUrl": restaurant.yelp_url,
            "yelpImgUrl": restaurant.yelp_img_url,
            "yelpRating": restaurant.yelp_rating,
            "yelpRatingImg": restaurant.yelp_rating_img,
            "reviewCount": restaurant.yelp_review_count,
            "lat": restaurant.lat,
            "lng": restaurant.lng,
            "categories": [jsonpickle.encode(category)
                           for category in restaurant.categories]
        }
        for restaurant in Restaurant.query.all()}

    return jsonify(restaurants)


@app.route('/register')
def register_user():
  """Allow user to register."""

  return render_template('register.html')


@app.route('/registered', methods=["POST"])
def add_user_to_db():
    """Add new user to table users."""

    # Get form values
    username = request.form.get("username")
    password = request.form.get("password")
    password1 = request.form.get("password1")
    fname = request.form.get("fname")
    lname = request.form.get("lname")

    # Get list of usernames in database model
    db_usernames = db.session.query(User.username).all()
    usernames = []
    for u in db_usernames:
        print u

    if username in usernames:
        flash("Username taken. Please select another.")
        return redirect("/register")

    # Validate password
    elif password != password1:
        flash("Your passwords do not match!")
        return redirect("/register")

    else: 
        # Instantiate new User object based on form values
        new_user = User(username=username,
                        password=password,
                        fname=fname,
                        lname=lname)

        # Add new User to db
        db.session.add(new_user)
        db.session.commit()

        # Redirect to homepage and confirm registration
        flash("You've successfully registered!")
        return redirect("/home")


@app.route('/login')
def login():
    """Login user."""
    
    return render_template("login.html")


@app.route('/loggedin', methods=["POST"])
def check_user_existence():
    """Allow user to login given correct credentials."""

    # Get form values
    username = request.form.get("username")
    password = request.form.get("password")

    # Get user object whose email matches form's email
    user = User.query.filter(User.username == username).one()

    # If email and password combo matches, logs in successfully
    if user and user.password == password:
        session["user_id"] = user.user_id
        flash("You've successfully logged in!")
        return redirect("/home")

    elif not user or user.password != form_password:
        flash("Invalid email or password. Please register if you do not have an account.")
        return redirect("/login")


@app.route('/account')
def user_detail():
    """Show information in user account."""

    # If user in session, get User object
    if session["user_id"]:
        user = User.query.filter(User.user_id == session["user_id"]).one()

    return render_template('account.html', user=user)


@app.route('/logout')
def logout():
    """Logout user."""

    del session["user_id"]
    flash("You've successfully logged out!")

    return redirect('/home')


if __name__ == "__main__":
    
    # Set debug=True here to invoke the DebugToolbarExtension later
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()