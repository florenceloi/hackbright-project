"""Utility file to seed hard-coded restaurants database from restaurants.txt in data/"""


# from sqlalchemy import func

from model import connect_to_db, db, Restaurant, Category, Restaurant_Category
from server import app


def load_restaurants():
    """Load restaurants from data/restaurants.txt into database"""

    print "Restaurants"

    for i, row in enumerate(open("data/restaurants.txt")):
        row = row.strip()
        name, address = row.split("|")
        print name + " " + address

        # Instantiate new Restaurant object based on unpacked row
        restaurant = Restaurant(name=name, address=address)

        # Add to database session (to be stored)
        db.session.add(restaurant)

        # Show how many records have been add (in increments of 10)
        if i % 10 == 0:
            print i

    # Commit the additions to the database
    db.session.commit()


if __name__ == "__main__":
    connect_to_db(app)
    db.create_all()

    load_restaurants()
