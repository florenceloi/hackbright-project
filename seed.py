"""Utility file to seed hard-coded restaurants database from restaurants.txt in data/"""


# from sqlalchemy import func

from model import connect_to_db, db, Restaurant
from server import app

from api import yelp_client


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


def import_yelp_restaurant_id():
    """Using restaurant name and address from hard-coded database,
    import restaurant id on Yelp"""

    params = {
        'term': 'dog friendly',
        'category_filter': 'restaurants'
    }

    sf_restaurants = yelp_client.search('San Francisco', **params)
    print sf_restaurants.total, "***************************************************"
    # print sf_restaurants, "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"

    db_restaurants = Restaurant.query.all()
    # print db_restaurants, "***************************************************"

    counter = 0

    # for restaurant in db_restaurants:
    #     for i in range(len(sf_restaurants)):
    #         print i, sf_restaurants[i].name
    #         if (restaurant.name == sf_restaurants[i].name and 
    #             restaurant.address == sf_restaurants[i].location.address):
    #                 counter += 1
    #                 print counter + ": " + restaurant.name + " " + restaurant.address


if __name__ == "__main__":
    connect_to_db(app)
    db.create_all()

    load_restaurants()
    import_yelp_restaurant_id()