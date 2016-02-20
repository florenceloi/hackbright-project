"""Utility file to seed database model"""

# from sqlalchemy import func

from model import connect_to_db, db, Restaurant
from server import app

from parse_restaurants import yelp_object_list


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


# def populate_categories_table(yelp_object_list):
#     """Takes in list of yelp restaurant objects and populates categories table."""

#     temp_category_dict = {}

#     # While looping over each category in each restaurant,
#     # adding category to temporary category_list if not already present
#     for yelp_object in yelp_object_list:
#         categories = yelp_object.categories
#         get_unique_categories(categories, temp_category_dict)

#     print temp_category_dict

#     # Looking over each unique category
#     for name, alias in temp_category_dict.iteritems():
#         new_category = Category(category=name,
#                                 alias=alias)

#         # Add new category to database session (to be stored)
#         db.session.add(new_category)

#     # Commit the additions to the database
#     db.session.commit()


# def populate_restaurant_categories_table(yelp_object_list):
#     """Takes in list of yelp restaurant objects and populates restaurant_categories table."""

#     # Get categories from database and their corresponding category ids
#     category_dict = get_category_and_id_dict()

#     # Get restaurant objects in database model
#     db_restaurants = Restaurant.query.all()

#     # Find database restaurant that corresponds to the yelp restaurant object,
#     # get database restaurant's restaurant id,
#     # get yelp restaurant object's categories
#     for restaurant in db_restaurants:

#         # Looping over each restaurant object from Yelp API call:
#         for yelp_object in yelp_object_list:
#             if yelp_object.id == restaurant.yelp_id:
#                 restaurant_id = restaurant.restaurant_id
#                 categories_for_current_restaurant = yelp_object.categories

#                 # Get corresponding category id for each category
#                 for category in categories_for_current_restaurant:
#                     category_id = category_dict[category[0]]

#                     # Instantiate new restaurant-category association
#                     new_association = Restaurant_Category(restaurant_id=restaurant_id,
#                                                           category_id=category_id)

#                     # Add new association to database
#                     db.session.add(new_association)

#     # Commit the additions to the database
#     db.session.commit()


###############################################################################
# Helper Functions

# def get_unique_categories(categories, temp_category_dict):
#     """Takes in a list of categories and returns a list of unique categories."""

#     # While looping over each category in each restaurant,
#     # adding category to temporary category_list if not already present
#     for category in categories:
#         name = category.name
#         alias = category.alias

#         if name in temp_category_dict:
#             continue

#         elif name not in temp_category_dict:
#             temp_category_dict[name] = alias

#     return temp_category_dict


# def get_category_and_id_dict():
#     """Returns a dictionary of category-category id key-value pairs from categories table."""

#     category_dict = {}

#     # Get all categories in database
#     db_category_list = Category.query.all()

#     # Get dictionary of category-category id key-value pairs
#     for category in db_category_list:
#         category_id = category.category_id
#         category = category.category
#         category_dict[category] = category_id

#     return category_dict


if __name__ == "__main__":
    connect_to_db(app)
    db.create_all()

    populate_restaurants_table(yelp_object_list)
    # populate_categories_table(yelp_object_list)
    # populate_restaurant_categories_table(yelp_object_list)
