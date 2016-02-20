from parse_restaurants import yelp_object_list

def get_unique_categories(yelp_object_list):
    """Takes in list of yelp restaurant objects and populates categories table."""

    unique_categories_list = {}

    # While looping over each category in each restaurant,
    # adding category to temporary category_list if not already present
    for yelp_object in yelp_object_list:
        categories = yelp_object.categories

        for category in categories:
            name = category.name

            if name not in unique_categories_list:
                unique_categories_list[name] = alias

            if name in unique_categories_list:
                continue

            elif name not in unique_categories_list:
                unique_categories_list[name] = alias
        get_unique_categories(categories, unique_categories_list)

def get_unique_categories(categories, unique_categories_list):
    """Takes in a list of categories and returns a list of unique categories."""

    # While looping over each category in each restaurant,
    # adding category to temporary category_list if not already present
    for category in categories:
        name = category.name
        alias = category.alias

        if name in unique_categories_list:
            continue

        elif name not in unique_categories_list:
            unique_categories_list[name] = alias

    return unique_categories_list
