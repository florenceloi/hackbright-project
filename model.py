"""Utility file to create database model"""

import os
from flask_sqlalchemy import SQLAlchemy

# Using the Flask-SQLAlchemy helper library, this allows us to connect to the
# PostgreSQL database (db). Its 'session' object allows us to interact with db.
db = SQLAlchemy()


###############################################################################
# Model definitions

class User(db.Model):
    """Registered user in website."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String(64), nullable=False)
    password = db.Column(db.String(64), nullable=False)
    fname = db.Column(db.String(64), nullable=False)
    lname = db.Column(db.String(64), nullable=False)

    def __repr__(self):
        """Provides helpful representation when printed."""

        return "<User user_id=%s username=%s fname=%s lname=%s>" % (self.user_id,
                                                                    self.username,
                                                                    self.fname,
                                                                    self.lname)


class Restaurant(db.Model):
    """Dog-friendly restaurants."""

    __tablename__ = "restaurants"

    restaurant_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(30), nullable=False)
    state_code = db.Column(db.String(2), nullable=False)
    country_code = db.Column(db.String(2), nullable=False)
    phone = db.Column(db.String(14), nullable=False, unique=True)
    yelp_id = db.Column(db.String(100), nullable=False, unique=True)
    ds_yelp_id = db.Column(db.String(100), unique=True)
    yelp_url = db.Column(db.String(200), nullable=False, unique=True)
    yelp_img_url = db.Column(db.String(200), nullable=False, unique=True)
    yelp_rating = db.Column(db.Float, nullable=False)
    yelp_rating_img = db.Column(db.String(200), nullable=False)
    yelp_review_count = db.Column(db.Integer, nullable=True)
    lat = db.Column(db.Float, nullable=False)
    lng = db.Column(db.Float, nullable=False)

    categories = db.relationship("Category",
                                 secondary="restaurant_categories",
                                 backref="restaurants")

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Restaurant restaurant_id=%s name=%s address=%s>" % (
            self.restaurant_id,
            self.name,
            self.address)


class Category(db.Model):
    """Possible food categories for restaurants."""

    __tablename__ = "categories"

    category_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    category = db.Column(db.String(64), nullable=False, unique=True)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Category category_id=%s category=%s alias=%s>" % (self.category_id,
                                                                   self.category)


class Review(db.Model):
    """Single user's review for particular restaurant."""

    __tablename__ = "reviews"

    review_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    restaurant_id = db.Column(db.Integer,
                              db.ForeignKey('restaurants.restaurant_id'),
                              nullable=False)
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.user_id'),
                        nullable=False)
    rating = db.Column(db.Float, nullable=False)
    body = db.Column(db.String(2000), nullable=False)

    user = db.relationship('User', backref=db.backref('reviews'))
    restaurant = db.relationship('Restaurant', backref=db.backref('reviews'))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Review id=%s restaurant_id=%s user_id=%s rating=%s>" % (
            self.review_id,
            self.restaurant_id,
            self.user_id,
            self.rating)


class Yelp_Review(db.Model):
    """Single Yelp review for particular restaurant."""

    __tablename__ = "yelp_reviews"

    yelp_review_id = db.Column(db.Integer,
                               autoincrement=True,
                               primary_key=True)
    ds_yelp_id = db.Column(db.String(100),
                           db.ForeignKey('restaurants.ds_yelp_id'),
                           nullable=False)
    rating = db.Column(db.Float, nullable=False)
    body = db.Column(db.String(5000), nullable=False)

    restaurant = db.relationship('Restaurant',
                                 backref=db.backref('yelp_reviews'))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Yelp_Review yelp_review_id=%s ds_yelp_id=%s>" % (
            self.yelp_review_id,
            self.ds_yelp_id)


class SA_Score(db.Model):
    """Sentiment analysis scores (dog, food, service) for each restaurant."""

    __tablename__ = "sa_scores"

    sa_score_id = db.Column(db.Integer,
                            autoincrement=True,
                            primary_key=True)
    restaurant_id = db.Column(db.Integer,
                              db.ForeignKey('restaurants.restaurant_id'),
                              nullable=False)
    dog_score = db.Column(db.Float, nullable=False)
    food_score = db.Column(db.Float, nullable=False)
    other_score = db.Column(db.Float, nullable=False)

    restaurant = db.relationship('Restaurant',
                                 backref=db.backref('sa_scores'))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<SA_Score sa_score_id=%s restaurant_id=%s>" % (
            self.sa_score_id,
            self.restaurant_id)

###############################################################################
# Association tables

class Favorite(db.Model):
    """One of single user's favorite restaurants."""

    __tablename__ = "favorites"

    favorite_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    restaurant_id = db.Column(db.Integer,
                              db.ForeignKey('restaurants.restaurant_id'),
                              nullable=False)
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.user_id'),
                        nullable=False)

    user = db.relationship('User', backref=db.backref('favorites'))
    restaurant = db.relationship('Restaurant', backref=db.backref('favorites'))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Favorite favorite_id=%s restaurant_id=%s user_id=%s>" % (
            self.favorite_id,
            self.restaurant_id,
            self.user_id)


class Restaurant_Category(db.Model):
    """Association class for restaurants and food categories."""

    __tablename__ = "restaurant_categories"

    restaurant_category_id = db.Column(db.Integer,
                                       autoincrement=True,
                                       primary_key=True)
    restaurant_id = db.Column(db.Integer,
                              db.ForeignKey('restaurants.restaurant_id'),
                              nullable=False)
    category_id = db.Column(db.Integer,
                            db.ForeignKey('categories.category_id'),
                            nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Rest_Cat id=%s restaurant_id=%s category_id=%s>" % (
            self.restaurant_category_id,
            self.restaurant_id,
            self.category_id)


##############################################################################
# Helper functions


def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configuration to use PostgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'postgresql:///r')
    # app.config['SQLALCHEMY_ECHO'] = True
    db.app = app
    db.init_app(app)


if __name__ == "__main__":

    # Allows us to interact with the database directly in interactive mode.
    from server import app
    connect_to_db(app)
    print "Connected to DB."
