from jinja2 import StrictUndefined

from flask import Flask, render_template, redirect, request, flash, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension

from model import (connect_to_db,
                   db,
                   User,
                   Restaurant,
                   Category,
                   Favorite,
                   Review)

from api import gmaps_key

import operator

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

    # import pdb; pdb.set_trace()
    # Instantiate city set using set comprehension
    # locations = {(r.country_code, r.state_code, r.city)
    #              for r in Restaurant.query.all()}
    locations = {(r.city, states_dict[r.state_code], r.country_code)
                 for r in Restaurant.query.all()}
    print locations

    # us_locations = {(l[0], l[1]) for l in locations if l[2] == "US"}
    # ca_locations = {(l[0], l[1]) for l in locations if l[2] == "CA"}

    # us_locations = sorted(us_locations, key=lambda us_location: us_location[1])
    # ca_locations = sorted(ca_locations, key=lambda ca_location: ca_location[1])

    # Instantiate category list using list comprehension
    categories = [category.category
                  for category in Category.query.order_by('category').all()]

    return render_template("home.html",
                           gmaps_key=gmaps_key,
                           locations=locations,
                           # us_locations=us_locations,
                           # ca_locations=ca_locations,
                           categories=categories)


@app.route('/home.json')
def bear_info():
    """JSON information about restaurants.
    For each category that each restaurant in the database is in,
    create a key-value pair in the restaurants dictionary,
    where the value is a dictionary containing restaurant information."""

    restaurants_lst = []

    # Get all restaurants in database
    restaurants = Restaurant.query.all()

    # For each restaurant, get a list of its categories
    for r in restaurants:
        categories = [category.category for category in r.categories]

        for i in range(len(categories)):
            restaurants_lst.append({"db_id": r.restaurant_id,
                                    "_name": r.name,
                                    "address": r.address,
                                    "phone": r.phone,
                                    "yelpUrl": r.yelp_url,
                                    "yelpImgUrl": r.yelp_img_url,
                                    "yelpRating": r.yelp_rating,
                                    "yelpRatingImg": r.yelp_rating_img,
                                    "reviewCount": r.yelp_review_count,
                                    "lat": r.lat,
                                    "lng": r.lng,
                                    "category": categories[i]})

    restaurants_dict = {"restaurants": restaurants_lst}

    return jsonify(restaurants_dict)


@app.route('/home.json')
def restaurant_info():
    """JSON information about restaurants.

    For each category that each restaurant in the database is in,
    create a key-value pair in the restaurants dictionary,
    where the value is a dictionary containing restaurant information."""

    restaurants_lst = []

    # Get all restaurants in database

    # sf_restaurant_list = Restaurant.query.filter(Restaurant.source == "hardcode").all()

    db_restaurant_list = Restaurant.query.all()

    # Match restaurant in yelp list with database list,
    # then grab restaurant id from database,
    # and get list of restaurant categories.
    for y in yelp_object_list:
        for s in sf_restaurant_list:
            if y.id == s.yelp_id:
                db_id = s.restaurant_id
        # categories = [category.category for category in r.categories]
        restaurant_categories = y.categories

        for i in range(len(restaurant_categories)):
            restaurants_lst.append({"db_id": db_id,
                                    "_name": y.name,
                                    "address": y.location.address[0],
                                    "phone": y.display_phone,
                                    "yelpUrl": y.url,
                                    "yelpImgUrl": y.image_url,
                                    "yelpRatingImg": y.rating_img_url_small,
                                    "reviewCount": y.review_count,
                                    "lat": y.location.coordinate.latitude,
                                    "lng": y.location.coordinate.longitude,
                                    "category": restaurant_categories[i].name})

    restaurants_dict = {"restaurants": restaurants_lst}
    return jsonify(restaurants_dict)


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
    for u_tuple in db_usernames:
        for u_username in u_tuple:
            usernames.append(u_username)

    # Verify username is not already in database
    if username in usernames:
        flash("Username taken. Please select another.")
        return redirect("/register")

    # Validate password
    elif password != password1:
        flash("Passwords do not match.")
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

        # Add user's id and first name to session
        db_user = User.query.filter(User.username == username,
                                    User.password == password).one()
        session["user_id"] = db_user.user_id
        session["fname"] = db_user.fname

        # Redirect to homepage and confirm registration
        flash("User %s added." % fname)
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
    user = User.query.filter(User.username == username).first()

    # If email and password combo matches, logs in successfully
    if user and user.password == password:
        session["user_id"] = user.user_id
        session["fname"] = user.fname

        flash("Welcome back, %s." % user.fname)
        return redirect("/home")

    elif not user or user.password != password:
        flash("Invalid email or password. Please register if you do not have an account.")
        return redirect("/login")


@app.route('/favorite')
def add_favorite():
    """Add user's favorite restaurant to database."""

    restaurant_id = int(request.args.get("restaurant_id"))
    restaurant = Restaurant.query.filter(Restaurant.restaurant_id == restaurant_id).one()

    if not session.get("user_id"):
        flash("Please sign in or register to favorite %s" % restaurant.name)
        return redirect("/login")

    else:

        user_id = session["user_id"]

        # Get list of user's favorites from database
        db_user_favorites = db.session.query(Favorite.restaurant_id).filter(User.user_id == user_id).all()
        user_favorites = []
        for u_tuple in db_user_favorites:
            for u_favorite in u_tuple:
                user_favorites.append(u_favorite)

        # If current restaurant is not already one of user's favorites,
        # add it to the database
        if restaurant_id not in user_favorites:
            new_favorite = Favorite(restaurant_id=restaurant_id,
                                    user_id=user_id)

            db.session.add(new_favorite)
            db.session.commit()

            flash("Saved %s as a favorite" % restaurant.name)

        return redirect("/home")


@app.route('/profile')
def user_detail():
    """Show information in user profile."""

    # If user in session, get User object
    if session["user_id"]:
        user_id = session["user_id"]
        user = User.query.filter(User.user_id == user_id).one()

        # Get favorites
        db_fav_restaurants = Favorite.query.filter(Favorite.user_id == user_id).all()

        fav_restaurants_dict = {}

        for d in db_fav_restaurants:
            yelp_id = d.restaurant.yelp_id
            restaurant_id = d.restaurant_id
            name = d.restaurant.name

            restaurant_dict = {"r_id": restaurant_id,
                               "name": name}

            fav_restaurants_dict[yelp_id] = restaurant_dict

        # Get reviews
        db_reviews = Review.query.filter(Review.user_id == user_id).all()

        reviews_dict = {}

        for d in db_reviews:
            yelp_id = d.restaurant.yelp_id
            name = d.restaurant.name
            restaurant_id = d.restaurant_id
            rating = d.rating
            body = d.body

            rev_dict = {"name": name,
                        "r_id": restaurant_id,
                        "rating": rating,
                        "body": body}

            reviews_dict[yelp_id] = rev_dict

        return render_template('profile.html',
                               user=user,
                               favorites=fav_restaurants_dict,
                               reviews=reviews_dict)

    else:
        flash("Please register first.")
        return redirect("/register")


@app.route('/restaurants/<int:restaurant_id>')
def review_restaurant(restaurant_id):
    """Allow user to review specific restaurant."""

    restaurant = Restaurant.query.filter(Restaurant.restaurant_id == restaurant_id).one()

    if not session.get("user_id"):

        flash("Please sign in or register to review %s" % restaurant.name)
        return redirect("/login")

    else:

        return render_template("restaurant-info.html",
                               restaurant=restaurant,
                               name=restaurant.name)


@app.route('/restaurants/<int:restaurant_id>/review', methods=["POST"])
def process_review(restaurant_id):
    """Add user's review to database."""

    # Get restaurant id, rating, review, and user_id
    rating = float(request.form.get("rating"))
    body = request.form.get("review-body")
    user_id = session["user_id"]

    # Get list of user's favorites from database
    db_user_reviews = db.session.query(Review.restaurant_id).filter(User.user_id == user_id).all()
    reviewed_restaurants = []
    for u_tuple in db_user_reviews:
        for u_review in u_tuple:
            reviewed_restaurants.append(u_review)

    restaurant = Restaurant.query.filter(Restaurant.restaurant_id == restaurant_id).one()

    # If current restaurant has not already been reviewed,
    # add current review to the database
    if restaurant_id not in reviewed_restaurants:
        new_review = Review(restaurant_id=restaurant_id,
                            user_id=user_id,
                            rating=rating,
                            body=body)

        db.session.add(new_review)
        db.session.commit()

        flash("Your review of %s has been saved." % restaurant.name)

    else:
        flash("Oops! Looks like you've already reviewed %s." % restaurant.name)

    return redirect("/home")


@app.route('/analysis')
def display_overall_scores():
    """Display overall sentiment analysis scores."""

    # Instantiate city set using set comprehension
    locations = {(r.state_code, states_dict[r.state_code], r.country_code)
                  for r in Restaurant.query.all() if r.state_code != 'CA'}
    print locations
    us_locations = {l[0]: l[1] for l in locations if l[2] == "US"}
    ca_locations = {l[0]: l[1] for l in locations if l[2] == "CA"}

    us_locations = sorted(us_locations.items(), key=operator.itemgetter(1))
    ca_locations = sorted(ca_locations.items(), key=operator.itemgetter(1))

    return render_template("sa-score-states.html",
                           us_locations=us_locations,
                           ca_locations=ca_locations)


@app.route('/analysis.json')
def import_overall_scores():
    """JSON information on overall sentiment analysis scores."""

    QUERY = """SELECT restaurants.state_code,
                      restaurants.country_code,
                      avg(sa_scores.dog_score) as avg_dog_score,
                      avg(sa_scores.food_score) as avg_food_score,
                      avg(sa_scores.other_score) as avg_other_score
               FROM sa_scores
               JOIN restaurants
                    USING (restaurant_id)
               GROUP BY (restaurants.state_code, restaurants.country_code)
               ORDER BY restaurants.state_code;
            """

    cursor = db.session.execute(QUERY)
    results = cursor.fetchall()

    score_data = []

    for r in results:
        state = states_dict[r[0]]
        location = state + ", " + r[1]
        score_data.append({"State": location,
                           "score": {"dog_score": r[2],
                                     "food_score": r[3],
                                     "other_score": r[4]}})

    scoreData_dict = {"scoreData": score_data}

    return jsonify(scoreData_dict)


@app.route('/analysis/state')
def display_state_scores():
    """Display state-level sentiment analysis scores."""

    state = request.args.get("location")
    session["state"] = state

    # Instantiate city set using set comprehension
    locations = {r.city for r in Restaurant.query.all() if r.state_code == state}

    locations = sorted(list(locations))

    return render_template("sa-score-cities.html",
                           state=state,
                           locations=locations)


@app.route('/analysis/state.json')
def import_state_scores():
    """JSON information on state-level sentiment analysis scores."""

    state = session["state"]

    QUERY = """SELECT restaurants.city,
                      avg(sa_scores.dog_score) as avg_dog_score,
                      avg(sa_scores.food_score) as avg_food_score,
                      avg(sa_scores.other_score) as avg_other_score
               FROM sa_scores
               JOIN restaurants
                    USING (restaurant_id)
               WHERE restaurants.state_code = '%s'
               GROUP BY (restaurants.city)
               ORDER BY restaurants.city;
            """ % state

    cursor = db.session.execute(QUERY)
    results = cursor.fetchall()

    score_data = []

    for r in results:
        score_data.append({"State": r[0],
                           "score": {"dog_score": r[1],
                                     "food_score": r[2],
                                     "other_score": r[3]}})

    scoreData_dict = {"scoreData": score_data}

    return jsonify(scoreData_dict)


@app.route('/analysis/state/city')
def display_city_scores():
    """Display city-level sentiment analysis scores."""

    city = request.args.get("location")
    session["city"] = city

    return render_template("sa-score-restaurants.html", city=city)


@app.route('/analysis/state/city.json')
def import_city_scores():
    """JSON information on city-level sentiment analysis scores."""

    city = session["city"]

    QUERY = """SELECT restaurants.name,
                      avg(sa_scores.dog_score) as avg_dog_score,
                      avg(sa_scores.food_score) as avg_food_score,
                      avg(sa_scores.other_score) as avg_other_score
               FROM sa_scores
               JOIN restaurants
                    USING (restaurant_id)
               WHERE restaurants.city = '%s'
               GROUP BY (restaurants.name)
               ORDER BY restaurants.name;
            """ % city

    cursor = db.session.execute(QUERY)
    results = cursor.fetchall()

    score_data = []

    for r in results:
        score_data.append({"State": r[0],
                           "score": {"dog_score": r[1],
                                     "food_score": r[2],
                                     "other_score": r[3]}})

    scoreData_dict = {"scoreData": score_data}

    return jsonify(scoreData_dict)


@app.route('/logout')
def logout():
    """Logout user."""

    # Get user object whose email matches form's email
    if session["user_id"]:
        flash("See you next time, %s!" % session["fname"])
        del session["user_id"], session["fname"]

    return redirect("/home")


###############################################################################
# Helper functions/definitions
states_dict = {"AZ": "Arizona",
               "IL": "Illinois",
               "NC": "North Carolina",
               "NV": "Nevada",
               "ON": "Ontario",
               "PA": "Pennsylvania",
               "QC": "Quebec",
               "WI": "Wisconsin"}

# import pdb; pdb.set_trace()

if __name__ == "__main__":
    
    # Set debug=True here to invoke the DebugToolbarExtension later
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    # DebugToolbarExtension(app)

    app.run()