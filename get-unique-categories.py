from parse_restaurants import yelp_object_list

def populate_categories_table(yelp_object_list):
    """Takes in list of yelp restaurant objects and populates categories table."""

    temp_category_dict = {}

    # While looping over each category in each restaurant,
    # adding category to temporary category_list if not already present
    for yelp_object in yelp_object_list:
        categories = yelp_object.categories
        get_unique_categories(categories, temp_category_dict)

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