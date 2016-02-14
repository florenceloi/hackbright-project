from jinja2 import StrictUndefined

from flask import Flask, render_template, redirect, request, flash, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension

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


# @app.route('/home.json')
# def bear_info():
#     """JSON information about restaurants."""

#     # Instantiate restaurant dictionary using dictionary comprehension
#     restaurants = {
#         restaurant.restaurant_id: {
#             "_name": restaurant.name,
#             "address": restaurant.address,
#             "phone": restaurant.phone,
#             "yelpUrl": restaurant.yelp_url,
#             "yelpImgUrl": restaurant.yelp_img_url,
#             "yelpRating": restaurant.yelp_rating,
#             "yelpRatingImg": restaurant.yelp_rating_img,
#             "reviewCount": restaurant.yelp_review_count,
#             "lat": restaurant.lat,
#             "lng": restaurant.lng,
#             "categories": restaurant.restaurant_categories
#         }
#         for restaurant in Restaurant.query.all()}

#     return jsonify(restaurants)


@app.route('/home.json')
def bear_info():
    """JSON information about categories."""

    # Instantiate restaurant dictionary using dictionary comprehension
    categories = {
        Category.restaurant_id: {
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
            "categories": restaurant.restaurant_categories
        }
        for category in Category.query.all()}

    return jsonify(restaurants)


if __name__ == "__main__":
    
    # Set debug=True here to invoke the DebugToolbarExtension later
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()