"""Utility file to seed database model"""

# from sqlalchemy import func

from model import connect_to_db, db, Restaurant, Category
from server import app
from time import time

from api import yelp_client


def populate_restaurants_table():
    """Load restaurant info (name, address, phone, yelp_id) into database model

    Additional details:
    Importing name, address, phone from data/restaurants.txt
    Using phone, importing yelp_id from Yelp API"""

    yelp_object_list = []

    # Parse through restaurants.txt and clean/unpack data
    for i, row in enumerate(open("data/restaurants.txt")):
        row = row.strip()
        name, address, phone = row.split("|")

        # Reformat phone number from "(XXX) XXX-XXXX" to "+1XXXXXXXXXX"
        yelp_phone = "+1" + phone[1:4] + phone[6:9] + phone[10:]

        # Return response dictionary from Yelp API for given phone number
        # Print how long the API call took
        start_time = time() * 1000
        yelp_dict = yelp_client.phone_search(phone)
        elapsed_time = (time() * 1000) - start_time
        print "API request %d: %d ms" % (i, elapsed_time)

        # Return single business in response dictionary that matches the 
        # name and address from restaurants.txt
        yelp_object = validate_single_business(yelp_dict, name, address) 

        # Add yelp_object to yelp_object_list to be used later
        yelp_object_list.append(yelp_object)

        # Get restaurant information for each yelp_object
        yelp_id = yelp_object.id
        yelp_img_url = yelp_object.image_url
        yelp_rating = yelp_object.rating
        yelp_review_count = yelp_object.review_count
        lat = yelp_object.location.coordinate.latitude
        lng = yelp_object.location.coordinate.longitude

        # Instantiate new Restaurant object with unpacked data
        restaurant = Restaurant(name=name,
                                address=address,
                                phone=phone,
                                yelp_phone=yelp_phone,
                                yelp_id=yelp_id,
                                yelp_img_url=yelp_img_url,
                                yelp_rating=yelp_rating,
                                yelp_review_count=yelp_review_count,
                                lat=lat,
                                lng=lng)

        # Add new restaurant to database session (to be stored)
        db.session.add(restaurant)

    # Commit the additions to the database
    db.session.commit()

    return yelp_object_list


def populate_categories_table(yelp_object_list):
   
    # Initialize empty category_list
    category_list = []

    # Looping over each restaurant
    for yelp_object in yelp_object_list:
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


###############################################################################
# Helper Functions

def validate_single_business(yelp_dict, name, address):
    """Takes in dictionary of corresponding business(es) for phone number,
    returns single business with corresponding name and address."""

    if yelp_dict.total == 1:
        yelp_object = yelp_dict.businesses[0]
    elif yelp_dict.total > 1:
        for i in range(len(yelp_dict.businesses)):
            current_business = yelp_dict.businesses[i]
            yelp_name = current_business.name
            yelp_address = current_business.location.address
            if name == yelp_name and address in yelp_address:
                yelp_object = yelp_dict.businesses[i]   

    return yelp_object


if __name__ == "__main__":
    connect_to_db(app)
    db.create_all()

    yelp_object_list = populate_restaurants_table()
    populate_categories_table(yelp_object_list)