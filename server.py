import io, json
from yelp.client import Client
from yelp.oauth1_authenticator import Oauth1Authenticator
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

with io.open('yelp_secret.json') as cred:

    # Loads in yelp_secret.json
    creds = json.load(cred)

    # Instantiates Oauth1Authenticator object with API keys
    auth = Oauth1Authenticator(**creds)

    # Constructs client object using Oauth1Authenticator object
    client = Client(auth)


###############################################################################
# Model definitions

class User(db.Model):
    """User of website."""

    __tablename__ = "users"

    pass


class Restaurant(db.Model):
    """Dog-friendly restaurants."""

    __tablename__ = "restaurants"

    pass


###############################################################################
# Helper functions

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PostgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///restaurants'
    db.app = app
    db.init_app(app)


if __name__ == "main":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print "Connected to DB."