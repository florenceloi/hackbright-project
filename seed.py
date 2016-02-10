"""Utility file to seed hard-coded restaurants database from restaurants.txt in data/"""

# from sqlalchemy import func

from model import connect_to_db, db, Restaurant, Category
from server import app
from time import time

from api import yelp_client


def populate_restaurants_table():
    """Load restaurant info (name, address, phone, yelp_id) into restaurants table.

    Additional details:
    Importing name, address, phone from data/restaurants.txt
    Using phone, importing yelp_id from Yelp API"""

    print "Restaurants"

    # Parse through data/restaurants.txt and clean/unpack data
    for i, row in enumerate(open("data/restaurants.txt")):
        row = row.strip()
        name, address, phone = row.split("|")

        # Reformat phone number from "(XXX) XXX-XXXX" to "+1XXXXXXXXXX"
        phone = "+1" + phone[1:4] + phone[6:9] + phone[10:]

        # Import yelp_id, yelp_rating, yelp_review_count from Yelp API
        # and print how long each call takes
        start_time = time() * 1000
        yelp_object = yelp_client.phone_search(phone).businesses[0]
        elapsed_time = (time() * 1000) - start_time
        print "API request %d: %d ms" % (i, elapsed_time)

        yelp_id = yelp_object.id
        yelp_rating = yelp_object.rating
        yelp_review_count = yelp_object.review_count

        # Instantiate new Restaurant object with unpacked data
        restaurant = Restaurant(name=name,
                                address=address,
                                phone=phone,
                                yelp_id=yelp_id,
                                yelp_rating=yelp_rating,
                                yelp_review_count=yelp_review_count)

        # Add new restaurant to database session (to be stored)
        db.session.add(restaurant)

        # Show how many records have been add (in increments of 10)
        if i % 10 == 0:
            print i

    # Commit the additions to the database
    db.session.commit()


def populate_categories_table():

    # Get all restaurants from database
    db_restaurants = Restaurant.query.all()
    
    # Initialize empty category_list
    category_list = []

    # Looping over each restaurant
    for restaurant in db_restaurants:
        yelp_object = yelp_client.get_business(restaurant.yelp_id).business
        categories = yelp_object.categories

        # While looping over each category in each restaurant,
        # adding category to category_list if not already present
        for category in categories:
            name = category.name

            if name in category_list:
                continue

            elif name not in category_list:
                category_list.append(name)

    # Looking over each unique category
    for current_category in category_list:
        new_category = Category(category=current_category)

        # Add new category to database session (to be stored)
        db.session.add(new_category)

    # Commit the additions to the database
    db.session.commit()

      
if __name__ == "__main__":
    connect_to_db(app)
    # db.create_all()

    populate_restaurants_table()
    populate_categories_table()