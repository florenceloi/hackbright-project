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

    def __repr__(self):
        """Provides helpful representation when printed."""

        return "<User user_id=%s username=%s>" % (self.user_id, self.username)


class Restaurant(db.Model):
    """Dog-friendly restaurants."""

    __tablename__ = "restaurants"

    restaurant_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    review_count = db.Column(db.Integer, nullable=True)
    rating = db.Column(db.Float, nullable=True)

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
    category = db.Column(db.String(64), nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Category category_id=%s category=%s>" % (self.category_id, self.category)


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
    body = db.Column(db.String(2000), nullable=False)

    user = db.relationship('User', backref=db.backref('reviews'))
    restaurant = db.relationship('Restaurant', backref=db.backref('reviews'))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Review review_id=%s restaurant_id=%s user_id=%s>" % (
            self.review_id,
            self.restaurant_id,
            self.user_id)


class Restaurant_Category(db.Model):
    """Association class for restaurants and food categories."""

    __tablename__ = "restaurant_categories"

    restaurant_category_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    restaurant_id = db.Column(db.Integer,
        db.ForeignKey('restaurants.restaurant_id'),
        nullable=False)
    category_id = db.Column(db.Integer,
        db.ForeignKey('categories.category_id'),
        nullable=False)

    restaurants = db.relationship('Restaurant', backref=db.backref('restaurant_categories'))
    categories = db.relationship('Category', backref=db.backref('restaurant_categories'))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Restaurant_Category id=%s restaurant_id=%s category_id=%s>" % (
            self.restaurant_category_id,
            self.restaurant_id,
            self.category_id)


###############################################################################
# Helper functions

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configuration to use PostgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///restaurants'
    app.config['SQLALCHEMY_ECHO'] = True
    db.app = app
    db.init_app(app)


if __name__ == "__main__":

    # If in interactive mode, this allows us to interact with the database directly.
    from server import app
    connect_to_db(app)
    print "Connected to DB."