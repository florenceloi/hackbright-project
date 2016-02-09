"""Utility file to seed hard-coded restaurants database from restaurants.txt in data/"""


# from sqlalchemy import func

from model import connect_to_db, db, Restaurant
from server import app


def load_restaurants():
    """Load restaurants from data/restaurants.txt into database"""

    print "Restaurants"

    # Parse through data/restaurants.txt and clean/unpack data
    for i, row in enumerate(open("data/restaurants.txt")):
        row = row.strip()
        name, address = row.split("|")

        # Instantiate new Restaurant object with unpacked data
        restaurant = Restaurant(name=name, address=address)

        # Add new restaurant to database session (to be stored)
        db.session.add(restaurant)

        # Show how many records have been add (in increments of 10)
        if i % 10 == 0:
            print i

    # Commit the additions to the database
    db.session.commit()


def import_yelp_restaurant_info():
    """Using restaurant name and address from hard-coded database,
    import additional restaurant information from Yelp"""

    


if __name__ == "__main__":
    connect_to_db(app)
    db.create_all()

    load_restaurants()