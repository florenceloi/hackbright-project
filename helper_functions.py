from time import time
from api import yelp_client


def populate_restaurants_table():
    """Parse restaurants.txt and return list of single Yelp restaurant objects.

    For each Yelp API phone_search response,
    select only the restaurant object with matching name and address.
    """

    yelp_object_list = []

    # Parse restaurants.txt and clean/unpack data
    for i, row in enumerate(open("data/sample-restaurants.txt")):
        row = row.strip()
        name, address, phone = row.split("|")

        # Return response dictionary from Yelp API for given phone number
        # Print how long the API call took
        start_time = time() * 1000
        yelp_dict = yelp_client.phone_search(phone)
        elapsed_time = (time() * 1000) - start_time
        print "API request %d: %d ms" % (i, elapsed_time)

        # Return single business in response dictionary that matches the
        # name and address from restaurants.txt
        if yelp_dict.total == 1:
            yelp_object = yelp_dict.businesses[0]
        elif yelp_dict.total > 1:
            for i in range(len(yelp_dict.businesses)):
                current_business = yelp_dict.businesses[i]
                yelp_name = current_business.name
                yelp_address = current_business.location.address
                if name == yelp_name and address in yelp_address:
                    yelp_object = yelp_dict.businesses[i]

        # Add yelp_object to yelp_object_list to be used later
        yelp_object_list.append(yelp_object)

    return yelp_object_list


def get_unique_categories(yelp_object_list):
    """Takes in list of yelp restaurant objects and populates categories table."""

    category_dict = {}

    # While looping over each category in each restaurant,
    # adding category to temporary category_dict if not already present
    for yelp_object in yelp_object_list:
        categories = yelp_object.categories

        for category in categories:
            name = category.name
            alias = category.alias

            if name not in category_dict:
                category_dict[name] = alias

            else:
                continue

    return category_dict


###############################################################################
# Calling the functions

yelp_object_list = populate_restaurants_table()
category_dict = get_unique_categories(yelp_object_list)
