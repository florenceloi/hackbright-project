"""Utility file to seed database model"""

from time import time
from model import connect_to_db, db, Restaurant, Category, Restaurant_Category, Yelp_Review
from server import app
from api import yelp_client
import json
import sqlalchemy


def import_restaurants_from_hardcode_list():
    """Load restaurant info into database model.
    Additional details:
    Importing name, address, phone number from hard coded data/restaurants.txt
    Using phone number, importing restaurant information from Yelp API"""

    hc_yelp_object_list = []

    # Parse through restaurants.txt and clean/unpack data
    for i, row in enumerate(open("data/restaurants.txt")):
        row = row.strip()
        name, address, phone = row.split("|")

        # Reformat phone number from "(XXX) XXX-XXXX" to "+1XXXXXXXXXX"
        yelp_phone = "+1" + phone[1:4] + phone[6:9] + phone[10:]

        # Return response dictionary from Yelp API for given phone number
        # Print how long the API call took
        start_time = time() * 1000
        yelp_dict = yelp_client.phone_search(yelp_phone)
        elapsed_time = (time() * 1000) - start_time
        print "API request %d: %d ms" % (i, elapsed_time)


        # Return single business in response dictionary that matches the
        # name and address from restaurants.txt
        yelp_object = validate_single_business(yelp_dict, name, address)

        # Add yelp_object to hc_yelp_object_list to be used later
        hc_yelp_object_list.append(yelp_object)

        # Get restaurant information for each yelp_object
        yelp_id = yelp_object.id
        city = yelp_object.location.city
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
                                city=city,
                                phone=phone,
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

    return hc_yelp_object_list


def import_restaurants_from_dataset():
    """Import dog-friendly restaurant from Yelp Challenge Dataset."""

    ds_yelp_object_list = []

    # Parse through Yelp businesses dataset
    for i, b in enumerate(open('data/yelp_academic_dataset_business.json')):
        b = json.loads(b.strip())

        try:
            # Get only restaurant objects with dogs allowed attribute,
            # and get desired values
            if b["attributes"]["Dogs Allowed"] and "Restaurants" in b["categories"]:
                ds_yelp_id = b["business_id"]
                name = b["name"]
                lat = b["latitude"]
                lng = b["longitude"]

                # Get Yelp response object of businesses with matching coordinates
                start_time = time() * 1000
                yelp_objects = yelp_client.search_by_coordinates(lat, lng).businesses
                elapsed_time = (time() * 1000) - start_time
                print "Row %d: %d ms" % (i, elapsed_time)

                # Get only one restaurant object with matching name,
                # and get desired values
                for y in yelp_objects:
                    try:
                        if name == y.name:
                            address = y.location.address[0]
                            city = y.location.city
                            phone = "(" + y.phone[:3] + ") " + y.phone[3:6] + "-" + y.phone[6:]
                            yelp_id = y.id
                            yelp_url = y.url
                            yelp_img_url = y.image_url
                            yelp_rating = y.rating
                            yelp_rating_img = y.rating_img_url_small
                            yelp_review_count = y.review_count

                            # Add yelp_object to hc_yelp_object_list to be used later
                            ds_yelp_object_list.append(y)

                            # Instantiate new restaurant object and add to db.
                            restaurant = Restaurant(name=name,
                                                    address=address,
                                                    city=city,
                                                    phone=phone,
                                                    yelp_id=yelp_id,
                                                    ds_yelp_id=ds_yelp_id,
                                                    yelp_url=yelp_url,
                                                    yelp_img_url=yelp_img_url,
                                                    yelp_rating=yelp_rating,
                                                    yelp_rating_img=yelp_rating_img,
                                                    yelp_review_count=yelp_review_count,
                                                    lat=lat,
                                                    lng=lng)

                            db.session.add(restaurant)
                            db.session.commit()

                    except (sqlalchemy.exc.IntegrityError,
                            sqlalchemy.exc.DataError,
                            IndexError):
                        db.session.rollback()

        except KeyError:
            continue

    return ds_yelp_object_list


def import_reviews_from_dataset():
    """Import reviews for dog-friendly restaurants from Yelp Challenge Dataset."""

    # import pdb; pdb.set_trace()

    ds_yelp_id_set = {restaurant.ds_yelp_id
                      for restaurant
                      in Restaurant.query.filter(Restaurant.ds_yelp_id != None).all()}

    import pdb; pdb.set_trace()
    
    # Parse through Yelp reviews dataset
    for i, review in enumerate(open('data/yelp_academic_dataset_review.json')):
        
        review = json.loads(review.strip())

        ds_yelp_id = review["business_id"]

        # Get only review objects if restaurant is in db,
        # and get desired values
        if ds_yelp_id in ds_yelp_id_set:
            rating = review["stars"]
            body = review["text"]

            # Instantiate new restaurant object and add to db.
            review = Yelp_Review(ds_yelp_id=ds_yelp_id,
                                 rating=rating,
                                 body=body)

            # db.session.add(review)
            # db.session.commit()

        # Provide some sense of progress
        if i % 10000 == 0:
            print i

    
def populate_categories_table(yelp_object_list):
    """Takes in list of yelp restaurant objects and populates categories table."""

    temp_category_list = []

    # While looping over each category in each restaurant,
    # adding category to temporary category_list if not already present
    for yelp_object in yelp_object_list:
        categories = yelp_object.categories
        get_unique_categories(categories, temp_category_list)

    # Looking over each unique category
    for current_category in temp_category_list:
        new_category = Category(category=current_category)

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
# Helper functions

# import pdb; pdb.set_trace()

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


def get_unique_categories(categories, temp_category_list):
    """Takes in a list of categories and returns a list of unique categories."""

    # While looping over each category in each restaurant,
    # adding category to temporary category_list if not already present
    for category in categories:
        name = category.name

        if name in temp_category_list:
            continue

        elif name not in temp_category_list:
            temp_category_list.append(name)

    return temp_category_list


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
    # db.create_all()

    # hc_yelp_object_list = import_restaurants_from_hardcode_list()
    # ds_yelp_object_list = import_restaurants_from_dataset()
    # complete_yelp_object_list = hc_yelp_object_list + ds_yelp_object_list

    # populate_categories_table(complete_yelp_object_list)
    # populate_restaurant_categories_table(complete_yelp_object_list)

    import_reviews_from_dataset()