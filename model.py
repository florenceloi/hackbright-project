# HUGE FIXME!!! CAN ONLY STORE YELP'S BUSINESS ID, CANNOT STORE ANYTHING ELSE

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
    yelp_id = db.Column(db.String(100), nullable=False, unique=True)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Restaurant restaurant_id=%s yelp_id=%s>" % (
            self.restaurant_id,
            self.yelp_id)


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


##############################################################################
# Helper functions

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configuration to use PostgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///r'
    # app.config['SQLALCHEMY_ECHO'] = True
    db.app = app
    db.init_app(app)


if __name__ == "__main__":

    # Allows us to interact with the database directly in interactive mode.
    from server import app
    connect_to_db(app)
    print "Connected to DB."