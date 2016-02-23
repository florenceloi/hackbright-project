"""Utility file to seed database model"""

<<<<<<< HEAD
from time import time
from model import connect_to_db, db, Restaurant
from server import app
from api import yelp_client
import json
import sqlalchemy


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




# def import_restaurants_from_hardcode_list(yelp_object_list):
#     """Store Yelp id for yelp_object_list restaurants in database."""

#     for y in yelp_object_list:
#         yelp_id = y.id

#         # Instantiate new Restaurant object with unpacked data
#         restaurant = Restaurant(source="hardcode",
#                                 yelp_id=yelp_id)

#         # Add new restaurant to database session (to be stored)
#         db.session.add(restaurant)

#     # Commit the additions to the database
#     db.session.commit()


# def import_restaurants_from_datasest():
#     """Import dog-friendly restaurant from Yelp Challenge Dataset."""

#     for i, b in enumerate(open('data/yelp_academic_dataset_business.json')):
#         b = json.loads(b.strip())

#         try:
#             if b["attributes"]["Dogs Allowed"] and "Restaurants" in b["categories"]:
#                 ds_yelp_id = b["business_id"]
#                 name = b["name"]
#                 lat = b["latitude"]
#                 lng = b["longitude"]

#                 start_time = time() * 1000
#                 yelp_objects = yelp_client.search_by_coordinates(lat, lng).businesses
#                 elapsed_time = (time() * 1000) - start_time
#                 print "Row %d: %d ms" % (i, elapsed_time)

#                 for y in yelp_objects:
#                     try:
#                         if name == y.name:
#                             yelp_id = y.id

#                             df_restaurant = Restaurant(source="dataset",
#                                                        yelp_id=yelp_id,
#                                                        ds_yelp_id=ds_yelp_id,
#                                                        lat=lat,
#                                                        lng=lng)

#                             db.session.add(df_restaurant)
#                             db.session.commit()
#                     except sqlalchemy.exc.IntegrityError:
#                         db.session.rollback()

#         except KeyError:
#             continue


def populate_ds_restaurants_table():
    """Import dog-friendly restaurant from Yelp Challenge Dataset."""

    for i, b in enumerate(open('data/yelp_academic_dataset_business.json')):
        b = json.loads(b.strip())

        try:
            if b["attributes"]["Dogs Allowed"] and "Restaurants" in b["categories"]:
                ds_yelp_id = b["business_id"]
                name = b["name"]
                lat = b["latitude"]
                lng = b["longitude"]

                start_time = time() * 1000
                yelp_objects = yelp_client.search_by_coordinates(lat, lng).businesses
                elapsed_time = (time() * 1000) - start_time
                print "Row %d: %d ms" % (i, elapsed_time)

                for y in yelp_objects:
                    try: 
                        if name == y.name:
                            yelp_id = y.id

                            df_restaurant = DSRestaurant(ds_yelp_id=ds_yelp_id,
                                                         yelp_id=yelp_id,
                                                         lat=lat,
                                                         lng=lng)

                            db.session.add(df_restaurant)
                            db.session.commit()
                    except sqlalchemy.exc.IntegrityError:
                        db.session.rollback()

        except KeyError:
            continue


###############################################################################
# Helper Functions


if __name__ == "__main__":
    connect_to_db(app)
    db.create_all()

    populate_restaurants_table(yelp_object_list)
    populate_ds_restaurants_table()