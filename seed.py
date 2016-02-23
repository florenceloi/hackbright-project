"""Utility file to seed database model"""

# from sqlalchemy import func

from time import time
from model import connect_to_db, db, Restaurant, DSRestaurant
from server import app
from api import yelp_client
import json
import sqlachemy

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