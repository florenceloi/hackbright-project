import os

from jinja2 import StrictUndefined

from flask import Flask, render_template, redirect, request, flash, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension

from sqlalchemy.sql import func

from model import (connect_to_db,
                   db,
                   User,
                   Restaurant,
                   Category,
                   Favorite,
                   Review,
                   SA_Score)

# from normalize_scores import min_score, max_score, normalize_data

from api import gmaps_key

import operator, collections

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

    restaurant = request.args.get("restaurant")

    us_az_cities = {(r.city) for r in Restaurant.query.all()
                    if r.country_code == "US" and r.state_code == "AZ"}
    us_ca_cities = {(r.city) for r in Restaurant.query.all()
                    if r.country_code == "US" and r.state_code == "CA"}
    us_il_cities = {(r.city) for r in Restaurant.query.all()
                    if r.country_code == "US" and r.state_code == "IL"}
    us_nc_cities = {(r.city) for r in Restaurant.query.all()
                    if r.country_code == "US" and r.state_code == "NC"}
    us_nv_cities = {(r.city) for r in Restaurant.query.all()
                    if r.country_code == "US" and r.state_code == "NV"}
    us_pa_cities = {(r.city) for r in Restaurant.query.all()
                    if r.country_code == "US" and r.state_code == "PA"}
    us_wi_cities = {(r.city) for r in Restaurant.query.all()
                    if r.country_code == "US" and r.state_code == "WI"}
    ca_cities = {(r.city, states_dict[r.state_code])
                  for r in Restaurant.query.all() if r.country_code == "CA"}

    us_az_cities = sorted(us_az_cities)
    us_ca_cities = sorted(us_ca_cities)
    us_il_cities = sorted(us_il_cities)
    us_nc_cities = sorted(us_nc_cities)
    us_nv_cities = sorted(us_nv_cities)
    us_pa_cities = sorted(us_pa_cities)
    us_wi_cities = sorted(us_wi_cities)
    ca_cities = sorted(ca_cities)

    # Instantiate category list using list comprehension
    categories = [category.category
                  for category in Category.query.order_by('category').all()]

    selected_categories = ["American (New)", "American (Traditional)", "Breakfast & Brunch",
        "Chinese", "Diners", "French", "German", "Greek", "Indian", "Italian",
        "Japanese", "Korean", "Mediterranean", "Mexican", "Pizza", "Southern",
        "Steakhouse", "Thai", "Vietnamese"]

    return render_template("home.html",
                           gmaps_key=gmaps_key,
                           us_az_cities=us_az_cities,
                           us_ca_cities=us_ca_cities,
                           us_il_cities=us_il_cities,
                           us_nc_cities=us_nc_cities,
                           us_nv_cities=us_nv_cities,
                           us_pa_cities=us_pa_cities,
                           us_wi_cities=us_wi_cities,
                           ca_cities=ca_cities,
                           categories=categories,
                           selected_categories=selected_categories)


@app.route('/home.json')
def restaurant_info():
    """JSON information about restaurants.
    For each category that each restaurant in the database is in,
    create a key-value pair in the restaurants dictionary,
    where the value is a dictionary containing restaurant information."""

    restaurants_lst = []

    if session.get("user_id"):

        user_id = session["user_id"]

        stmt = db.session.query(Favorite.restaurant_id).filter(Favorite.user_id == 1).subquery()
        restaurants = db.session.query(Restaurant).outerjoin(stmt).all()

        for r in restaurants:

            # Get boolean value for whether user has favorited this restaurant
            if r.favorites:
                fav = True
            else:
                fav = False

            # Get a list of restaurant's categories
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
                                        "favorite": fav,
                                        "category": categories[i]})

    else:

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


@app.route('/get-recs')
def get_recs():
    """Given a city, get top restaurants from database for AJAX response"""
    # import pdb; pdb.set_trace()
    city = request.args.get("city")

    if city != "San Francisco":
        QUERY = """SELECT restaurants.restaurant_id,
                          restaurants.name,
                          restaurants.address,
                          restaurants.yelp_url,
                          sa_scores.norm_dog_score,
                          sa_scores.norm_food_score,
                          sa_scores.norm_other_score,
                          sa_scores.total_norm_score,
                          restaurants.city
                   FROM restaurants
                   JOIN sa_scores
                        USING (restaurant_id)
                   WHERE restaurants.city = '%s'
                   ORDER BY sa_scores.total_norm_score DESC
                   LIMIT 5;
                """ % (city)

        cursor = db.session.execute(QUERY)
        recommendations = cursor.fetchall()

        rec_list = []

        for r in recommendations:
            rec_list.append({"r_id": r[0],
                             "_name": r[1],
                             "address": r[2],
                             "yelpUrl": r[3],
                             "dog": r[4],
                             "food": r[5],
                             "other": r[6],
                             "total": r[7],
                             "city": r[8]})

    else:
        rec_list = ["San Francisco"]

    rec_dict = {"recs": rec_list}

    return jsonify(rec_dict)


@app.route('/get-reviews')
def get_reviews():
    """Given a restaurant id, get reviews from database for AJAX response"""

    restaurant_id = int(request.args.get("restaurant_id"))
    restaurant = Restaurant.query.filter(Restaurant.restaurant_id == restaurant_id).one()

    reviews = restaurant.reviews

    reviews_lst = []

    for r in reviews:
        reviews_lst.append({"username": r.user.username,
                            "rating": str(r.rating),
                            "_body": r.body})

    reviews_dict = {"name": restaurant.name,
                    "reviews": reviews_lst}

    return jsonify(reviews_dict)


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
        flash("Username taken. Please select another.", "error")
        return redirect("/register")

    # Validate password
    elif password != password1:
        flash("Passwords do not match.", "error")
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
        flash("User %s added." % fname, "success")
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

        flash("Welcome back, %s." % user.fname, "success")
        return redirect("/home")

    elif not user or user.password != password:
        flash("Invalid email or password. Please register if you do not have an account.", "error")
        return redirect("/login")


@app.route('/favorite')
def add_favorite():
    """Add user's favorite restaurant to database."""

    restaurant_id = int(request.args.get("restaurant_id"))
    restaurant = Restaurant.query.filter(Restaurant.restaurant_id == restaurant_id).one()

    if not session.get("user_id"):
        flash("Please sign in or register to favorite %s" % restaurant.name, "error")
        return redirect("/login")

    else:
        user_id = session["user_id"]

        # Get list of user's favorites from database
        db_user_favorites = Favorite.query.filter(Favorite.user_id == user_id).all()
        user_favorites = []
        for d in db_user_favorites:
            user_favorites.append(d.restaurant_id)

        # If current restaurant is not already one of user's favorites,
        # add it to the database
        if restaurant_id not in user_favorites:
            new_favorite = Favorite(restaurant_id=restaurant_id,
                                    user_id=user_id)

            db.session.add(new_favorite)
            db.session.commit()

        else:
            fav = Favorite.query.filter(Favorite.restaurant_id == restaurant_id,
                                        Favorite.user_id == user_id).one()

            db.session.delete(fav)
            db.session.commit()

        return str(restaurant_id)


@app.route('/profile')
def user_detail():
    """Show information in user profile."""

    # If user in session, get User object
    if session["user_id"]:
        user_id = session["user_id"]
        user = User.query.filter(User.user_id == user_id).one()

        # Get favorites
        db_fav_restaurants = Favorite.query.filter(Favorite.user_id == user_id).all()

        locations = []

        for d in db_fav_restaurants:
            city = d.restaurant.city
            state = states_dict[d.restaurant.state_code]
            location = city + ", " + state
            if location not in locations:
                locations.append(location)

        fav_restaurants_dict = {}

        for l in locations:
            fav_restaurants_dict[l] = []

        for d in db_fav_restaurants:
            restaurant_id = d.restaurant_id
            name = d.restaurant.name
            city = d.restaurant.city
            state = states_dict[d.restaurant.state_code]
            location = city + ", " + state

            restaurant_dict = {"r_id": restaurant_id,
                               "name": name}

            fav_restaurants_dict[location].append(restaurant_dict)

        for k, v in fav_restaurants_dict.items():
            v = sorted(v)
            fav_restaurants_dict[k] = v

        ordered_fav_restaurants_dict = collections.OrderedDict(sorted(fav_restaurants_dict.items()))

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
                               favorites=ordered_fav_restaurants_dict,
                               reviews=reviews_dict)

    else:
        flash("Please register first.", "error")
        return redirect("/register")


@app.route('/restaurants/<int:restaurant_id>')
def review_restaurant(restaurant_id):
    """Allow user to review specific restaurant."""

    restaurant = Restaurant.query.filter(Restaurant.restaurant_id == restaurant_id).one()

    if not session.get("user_id"):

        flash("Please sign in or register to review %s" % restaurant.name, "error")
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

    # Get list of user's reviews from database
    db_user_reviews = Review.query.filter(Review.user_id == user_id).all()
    reviewed_restaurants = []
    for d in db_user_reviews:
        reviewed_restaurants.append(d.restaurant_id)

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

        flash("Your review of %s has been saved." % restaurant.name, "success")

    else:
        flash("Oops! Looks like you've already reviewed %s." % restaurant.name, "error")

    return redirect("/home")


@app.route('/analysis')
def display_overall_scores():
    """Display overall sentiment analysis scores."""

    # Instantiate city set using set comprehension
    locations = {(r.state_code, states_dict[r.state_code], r.country_code)
                  for r in Restaurant.query.all() if r.state_code != 'CA'}

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
                      avg(sa_scores.norm_dog_score) as avg_dog_score,
                      avg(sa_scores.norm_food_score) as avg_food_score
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
                           "score": {"Dog Friendliness": r[2],
                                     "Food Quality": r[3]}})

    scoreData_dict = {"scoreData": score_data}

    return jsonify(scoreData_dict)


@app.route('/analysis/state')
def display_state_scores():
    """Display state-level sentiment analysis scores."""

    state = request.args.get("location")

    for abbrev, full in states_dict.iteritems():
        if full == state:
            abbrev_state = abbrev

    session["state"] = abbrev_state

    # Instantiate city set using set comprehension
    locations = {r.city for r in Restaurant.query.all() if r.state_code == abbrev_state}

    locations = sorted(list(locations))

    return render_template("sa-score-cities.html",
                           state=state,
                           locations=locations)


@app.route('/analysis/state.json')
def import_state_scores():
    """JSON information on state-level sentiment analysis scores."""

    state = session["state"]

    QUERY = """SELECT restaurants.city,
                      avg(sa_scores.norm_dog_score) as avg_dog_score,
                      avg(sa_scores.norm_food_score) as avg_food_score
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
                           "score": {"Dog Friendliness": r[1],
                                     "Food Quality": r[2]}})

    scoreData_dict = {"scoreData": score_data}

    return jsonify(scoreData_dict)


@app.route('/analysis/state/city')
def display_city_scores():
    """Display city-level sentiment analysis scores."""

    city = request.args.get("location")
    session["city"] = city

    abbrev_state = session["state"]
    state = states_dict[abbrev_state]

    return render_template("sa-score-restaurants.html",
                           city=city,
                           state=state)


@app.route('/analysis/state/city.json')
def import_city_scores():
    """JSON information on city-level sentiment analysis scores."""

    city = session["city"]

    QUERY = """SELECT restaurants.name,
                      avg(sa_scores.norm_dog_score) as avg_dog_score,
                      avg(sa_scores.norm_food_score) as avg_food_score
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
                           "score": {"Dog Friendliness": r[1],
                                     "Food Quality": r[2]}})

    scoreData_dict = {"scoreData": score_data}

    return jsonify(scoreData_dict)


@app.route('/logout')
def logout():
    """Logout user."""

    # Get user object whose email matches form's email
    if session["user_id"]:
        flash("See you next time, %s!" % session["fname"], "success")
        del session["user_id"], session["fname"]

    return redirect("/home")


###############################################################################
# Helper functions/definitions

# import pdb; pdb.set_trace()

states_dict = {"AZ": "Arizona",
               "CA": "California",
               "IL": "Illinois",
               "NC": "North Carolina",
               "NV": "Nevada",
               "ON": "Ontario",
               "PA": "Pennsylvania",
               "QC": "Quebec",
               "WI": "Wisconsin"}


if __name__ == "__main__":

    # Set debug=True here to invoke the DebugToolbarExtension later
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    # DebugToolbarExtension(app)
    port = int(os.environ.get('PORT', 5000))

    app.run(host='0.0.0.0', port=port)
