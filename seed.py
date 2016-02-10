"""Utility file to seed hard-coded restaurants database from restaurants.txt in data/"""


# from sqlalchemy import func

from model import connect_to_db, db, Restaurant
from server import app

from api import yelp_client


def load_restaurants_and_import_yelp_id():
    """Load restaurant info (name, address, phone, yelp_id) into database.

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
        yelp_object = yelp_client.phone_search(phone).businesses[0]
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

      
if __name__ == "__main__":
    connect_to_db(app)
    db.create_all()

    load_restaurants_and_import_yelp_id()