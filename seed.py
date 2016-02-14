"""Utility file to seed database model"""

# from sqlalchemy import func

from model import connect_to_db, db, Restaurant, Category, Restaurant_Category
from server import app
from time import time

from api import yelp_client


def populate_restaurants_table():
    """Load restaurant info into database model.

    Additional details:
    Importing name, address, phone number from hard coded data/restaurants.txt
    Using phone number, importing restaurant information from Yelp API"""

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
        yelp_url = yelp_object.url
        yelp_img_url = yelp_object.image_url
        yelp_rating = yelp_object.rating
        yelp_rating_img = yelp_object.rating_img_url_small
        yelp_review_count = yelp_object.review_count
        lat = yelp_object.location.coordinate.latitude
        lng = yelp_object.location.coordinate.longitude

        # Instantiate new Restaurant object with unpacked data
        restaurant = Restaurant(name=name,
                                address=address,
                                phone=phone,
                                yelp_phone=yelp_phone,
                                yelp_id=yelp_id,
                                yelp_url=yelp_url,
                                yelp_img_url=yelp_img_url,
                                yelp_rating=yelp_rating,
                                yelp_rating_img=yelp_rating_img,
                                yelp_review_count=yelp_review_count,
                                lat=lat,
                                lng=lng)

        # Add new restaurant to database session (to be stored)
        db.session.add(restaurant)

    # Commit the additions to the database
    db.session.commit()

    return yelp_object_list


def populate_categories_table(yelp_object_list):
    """Takes in list of yelp restaurant objects and populates categories table."""
   
    temp_category_dict = {}

    # While looping over each category in each restaurant,
    # adding category to temporary category_list if not already present
    for yelp_object in yelp_object_list:
        categories = yelp_object.categories
        get_unique_categories(categories, temp_category_dict)

    print temp_category_dict

    # Looking over each unique category
    for name, alias in temp_category_dict.iteritems():
        new_category = Category(category=name,
                                alias=alias)

        # Add new category to database session (to be stored)
        db.session.add(new_category)

    # Commit the additions to the database
    db.session.commit()


def populate_restaurant_categories_table(yelp_object_list):
    """Takes in list of yelp restaurant objects and populates restaurant_categories table."""

    # Get categories from database and their corresponding category ids
    category_dict = get_category_and_id_dict()

    # Get restaurant objects in database model
    db_restaurants = Restaurant.query.all()
        
    # Find database restaurant that corresponds to the yelp restaurant object,
    # get database restaurant's restaurant id,
    # get yelp restaurant object's categories
    for restaurant in db_restaurants:

        # Looping over each restaurant object from Yelp API call:
        for yelp_object in yelp_object_list:
            if yelp_object.id == restaurant.yelp_id:
                restaurant_id = restaurant.restaurant_id
                categories_for_current_restaurant = yelp_object.categories
        
                # Get corresponding category id for each category
                for category in categories_for_current_restaurant:
                    category_id = category_dict[category[0]]

                    # Instantiate new restaurant-category association
                    new_association = Restaurant_Category(restaurant_id=restaurant_id,
                                                          category_id=category_id)

                    # Add new association to database
                    db.session.add(new_association)

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


def get_unique_categories(categories, temp_category_dict):
    """Takes in a list of categories and returns a list of unique categories."""

    # While looping over each category in each restaurant,
    # adding category to temporary category_list if not already present
    for category in categories:
        name = category.name
        alias = category.alias

        if name in temp_category_dict:
            continue

        elif name not in temp_category_dict:
            temp_category_dict[name] = alias

    return temp_category_dict


def get_category_and_id_dict():
    """Returns a dictionary of category-category id key-value pairs from categories table."""

    category_dict = {}

    # Get all categories in database
    db_category_list = Category.query.all()  
   
    # Get dictionary of category-category id key-value pairs
    for category in db_category_list:
        category_id = category.category_id
        category = category.category
        category_dict[category] = category_id

    return category_dict


if __name__ == "__main__":
    connect_to_db(app)
    db.create_all()

    yelp_object_list = populate_restaurants_table()
    populate_categories_table(yelp_object_list)
    populate_restaurant_categories_table(yelp_object_list)