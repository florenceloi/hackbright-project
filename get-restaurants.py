import json

# def get_dog_friendly_restaurants():
"""Given JSON file path containing Yelp dataset, return JSON subset of dog-friendly restautants."""

df_restautants = open('data/yelp_academic_dataset_business.json')

# import pdb; pdb.set_trace()

for line in df_restautants:
    line = json.loads(line.strip())

    try:
        if line["attributes"]["Dogs Allowed"]:
            print line

    except KeyError:
        continue