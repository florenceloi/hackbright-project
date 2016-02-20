"""Utility file to seed database model"""

# from sqlalchemy import func

from model import connect_to_db, db, Restaurant
from server import app

from helper_functions import yelp_object_list


def populate_restaurants_table(yelp_object_list):
    """Store Yelp id for yelp_object_list restaurants in database."""

    for y in yelp_object_list:
        yelp_id = y.id

        # Instantiate new Restaurant object with unpacked data
        restaurant = Restaurant(yelp_id=yelp_id)

        # Add new restaurant to database session (to be stored)
        db.session.add(restaurant)

    # Commit the additions to the database
    db.session.commit()


###############################################################################
# Helper Functions


if __name__ == "__main__":
    connect_to_db(app)
    db.create_all()

    populate_restaurants_table(yelp_object_list)
